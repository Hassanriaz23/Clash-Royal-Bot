import scrapy
from ..functions import is_previous_war_day, is_today_war_day, utc_to_lt, cal_percentage, cal_win_defeat, \
    cal_win_defeat_single, is_match_diff_less_then_40sec
import xlsxwriter


class WinSpider(scrapy.Spider):
    name = "trial"
    allowed_domains = ["royaleapi.com"]
    start_urls = ["https://royaleapi.com/clan/8J2RQRYC/war/race"]
    victory = []
    defeat = []
    draw = []

    def parse(self, response):
        player_name = []
        player_in_clan_tags = []
        player_decks = []
        clan_name = response.css('.active_clan .item .name::text').get().strip()
        is_col_week = response.css('.active_clan .summary .medal::text').get().strip() == '0'
        for i, player in enumerate(response.css('tbody tr.player:not(.not_current_member)')):
            deck_used = int(player.css('td .decks_used_today::text').get().strip())
            if deck_used != 0:
                player_name = player_name + [player.css('.force_single_line_hidden::text').get().strip()]
                player_in_clan_tags = player_in_clan_tags + [
                    player.css('tr.player:not(.not_current_member)::attr("data-href")').get().split('/')[2].strip()]
                player_decks = player_decks + [deck_used]
                yield {'player name': player_name[i],
                       'player tag': player_in_clan_tags[i],
                       'deck used': player_decks[i]
                       }
            else:
                break

        for player in response.css('tbody tr.player.not_current_member'):
            deck_used = int(player.css('td .decks_used_today::text').get())
            if deck_used != 0:
                player_name = player_name + [player.css('.force_single_line_hidden::text').get().strip()]
                player_in_clan_tags = player_in_clan_tags + [
                    player.css('tr.player.not_current_member::attr("data-href")').get().split('/')[2].strip()]
                player_decks = player_decks + [deck_used]
                yield {'player name': player_name[(len(player_name) - 1)],
                       'player tag': player_in_clan_tags[(len(player_name) - 1)],
                       'deck used': player_decks[(len(player_name) - 1)]
                       }
            else:

                break

        for tag in player_in_clan_tags:
            war_1v1_url = "https://royaleapi.com/player/" + tag + "/battles/scroll/0/type/riverRacePvP"
            war_colduel_url = "https://royaleapi.com/player/" + tag + "/battles/scroll/0/type/riverRaceDuelColosseum"
            war_duel_url = "https://royaleapi.com/player/" + tag + "/battles/scroll/0/type/riverRaceDuel"
            if is_col_week:
                for url in [war_colduel_url, war_1v1_url]:
                    yield scrapy.Request(url, callback=self.crawl_player, meta={'clan_name': clan_name,
                                                                                'url': url})
            else:
                for url in [war_duel_url, war_1v1_url]:
                    yield scrapy.Request(url, callback=self.crawl_player, meta={'clan_name': clan_name,
                                                                                'url': url})

    def crawl_player(self, response):
        tag = response.meta.get('tag')
        is_col_week = response.meta.get('is_col_week')
        url = response.meta.get('url')
        clan_name = response.meta.get('clan_name')
        victory = []
        defeat = []
        draw = []
        matchtime_utc = []
        battles = response.css('.battle_list_battle')
        if len(battles) == 0:  # checks if thers is no data in this website (due to excessive playing) then crawl histoy url off that player.
            history_url = url.replace("/scroll/0/type/", "/history?battle_type=")
            yield scrapy.Request(history_url, callback=self.crawl_player, meta={'clan_name': clan_name})

        for i, battle in enumerate(battles):
            player_clan_name = response.css('.team-segment:nth-child(1) .battle_player_clan::text').get().strip()
            player_name = battle.css(
                '.team-segment:nth-child(1) .hover_highlight.single-line-truncate::text').get().strip()
            opp_clan_name = battle.css('.team-segment+ .team-segment .battle_player_clan::text').extract()
            opp_clan_name = "".join(opp_clan_name).strip().split(
                "\n\n")  # ["\nL'élite ", '@ge\n', "\nL'élite ", '@ge\n'] fix this issuen
            outcome = battle.css('.ribbon::text').get().strip()
            game_mode = battle.css('.game_mode_header::text').get().strip()
            matchtime_utc = matchtime_utc + [battle.css('.battle-timestamp-popup::attr("data-content")').get()]

            print(f"name: {opp_clan_name}, game mode: {game_mode}, outcome: {outcome}, time: {utc_to_lt(matchtime_utc[i])}")

            if is_today_war_day(matchtime_utc[i]):
                # to prevent duplicate battles an war matches in other clans
                if not (i != 0 and is_match_diff_less_then_40sec(matchtime_utc[i - 1], matchtime_utc[i])) and player_clan_name == clan_name:
                    # print("Duplicate asdasdas")
                    victory, defeat, draw = cal_win_defeat_single(victory, defeat, draw, game_mode, outcome,
                                                                  opp_clan_name)
                    print(f'Victory {victory}')
                    print(f'defeat {defeat}')
                    print(f'defeat {draw}')
            else:
                break

        self.victory = self.victory + victory
        self.defeat = self.defeat + defeat
        self.draw = self.draw + draw
        player_name = response.css('.team-segment:nth-child(1) .hover_highlight.single-line-truncate::text').get()
        yield {
            'player name': player_name,
            'victory': [len(victory), len(self.victory)],
            'defeat': [len(defeat), len(self.defeat)],
            'draw': [len(draw), len(self.draw)],
            "total": [len(victory) + len(defeat) + len(draw), len(self.victory) + len(self.defeat) + len(self.draw)]
        }

    def close(self, reason):
        # run once in the end of program
        print("in closed")

        all_match_count_sort, win_count, win_per, total_win_per, total_matches = cal_percentage(self.victory,
                                                                                                self.defeat)
        workbook = xlsxwriter.Workbook('Win_rate.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        center = workbook.add_format({'align': 'center'})
        percentage = workbook.add_format({'align': 'center', 'num_format': '0.0%'})
        left = workbook.add_format({'align': 'left'})
        worksheet.write('A1', 'Clan name', bold)
        worksheet.write('B1', 'Matches', bold)
        worksheet.write('C1', 'Wins', bold)
        worksheet.write('D1', 'Win %', bold)

        worksheet.write('A2', 'ALL', left)
        worksheet.write('B2', total_matches, center)
        worksheet.write('C2', len(self.victory), center)
        worksheet.write('D2', f"{total_win_per}%")
        row = 2
        col = 0
        for k in all_match_count_sort.keys():
            worksheet.write(row, col, k, left)
            worksheet.write(row, col + 1, all_match_count_sort[k], center)
            worksheet.write(row, col + 2, win_count[k], center)
            worksheet.write(row, col + 3, f"{win_per[k]}%")
            row += 1

        workbook.close()
