import pygame
from config import *
from util_functions import *


class Figure:
    def __init__(self,
                screen,    
                x, y, width, height,
                bg_color = BG_COLOR,
                font_size = FONT_SIZE
                ):
        '''
        screen: pygame display object where the chart is drawn
        xy:     starting position of Figure in pygame display object
        width:  width of Figure
        height: height of Figure
        '''
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.font = pygame.font.SysFont(None, font_size)

        self.background = pygame.Surface((self.width, self.height))
        self.title = Area(self)
        self.legend = Legend(self)
        self.yaxis_label = Area(self)
        self.xaxis_label = Area(self)
        self.xaxis_tick = xaxisTick(self)
        self.chart_area = ChartArea(self)


    def create_figure(self):
        self.screen.blit(self.background, (self.x, self.y))
        self.background.fill(self.bg_color)

    def set_title(self, title):
        self.title.add_text(title)
        self.title.width = self.width
        self.title.height = self.title.txt.get_height()

    def set_legend(self):
        self.legend.add_text('LEGEND') # to be replaced with proper legend
        self.legend.width = self.width
        self.legend.height = self.legend.txt.get_height()
        self.legend.y = self.height - self.legend.height

    def set_yaxis_label(self, label):
        self.yaxis_label.add_text_vertical(label)
        self.yaxis_label.width = self.yaxis_label.txt.get_width() 
        self.yaxis_label.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height)
        self.yaxis_label.x = 0
        self.yaxis_label.y = self.title.height

    def set_xaxis_label(self, label):
        self.xaxis_label.add_text(label)
        self.xaxis_label.width = self.width - self.yaxis_label.width
        self.xaxis_label.height = self.xaxis_label.txt.get_height()
        self.xaxis_label.x = self.yaxis_label.width
        self.xaxis_label.y = self.height - (self.legend.height + self.xaxis_label.height)
    
    def set_xaxis_tick(self):
        self.xaxis_tick.width = self.width - self.yaxis_label.width
        self.xaxis_tick.height = 20 # to be calculated later
        self.xaxis_tick.x = self.yaxis_label.width
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height - self.height)
        
    def set_chart_area(self):
        self.chart_area.width = self.width - self.yaxis_label.width
        self.chart_area.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.chart_area.x = self.yaxis_label.width
        self.chart_area.y = self.title.height

    def draw_figure(self):
        for area in [self.title, self.legend, self.yaxis_label, self.xaxis_label, self.chart_area, self.xaxis_tick]:
            area.draw()

    def line(self, name, x, y, color=None, line_width=1): # for now accept only list
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%8]
            
        check = check_list_xy(x, y)
        if check:
            if name not in self.chart_area.chart_names:
                self.chart_area.charts.append(Line(name, x, y, color, line_width))
                self.chart_area.chart_names.append(name)
            else:
                self.update_chart(name, x, y)

    def bar(self, name, x, y, color=None, bar_width=20):# for now accept only list
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%8]

        check = check_list_xy(x, y)
        if check:
            if name not in self.chart_area.chart_names:
                self.chart_area.charts.append(Bar(name, x, y, color, bar_width))
                self.chart_area.chart_names.append(name)
            else:
                self.update_chart(name, x, y)
    
    def update_chart(self, name, x, y):
        chart = [i for i in self.chart_area.charts if i.name == name][0]
        chart.x = x
        chart.y = y

        
        
class Area:
    def __init__(self, figure):
        '''
        figure: pygameChart Figure object
        '''
        self.figure = figure
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        
    def add_text(self, text):
        self.txt = self.figure.font.render(text, True, TEXT_COLOR)
        self.txt_rect = self.txt.get_rect(center = (self.x + self.width / 2, self.y + self.height / 2))
    
    def add_text_vertical(self, text):
        self.txt = self.figure.font.render(text, True, TEXT_COLOR)
        self.txt = pygame.transform.rotate(self.txt, 90)
        self.txt_rect = self.txt.get_rect(center = (self.x + self.width / 2, self.y + self.height / 2))

    def draw(self): 
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, self.figure.bg_color, self.rect)
        if ('txt' in dir(self)) & ('txt_rect' in dir(self)):
            self.figure.background.blit(self.txt, self.txt_rect)
        

        
class Legend(Area):
    def __init__(self, figure):
        super().__init__(figure)

class xaxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)
    
    def draw(self):
        # chart borders for now. requires margin from axis labels and/or title
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, (0,0,0), self.rect, width=1)




class ChartArea(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.charts = []
        self.chart_names = []
        self.chart_margin = 25 # should be optimized
    
    def draw(self):
        # chart borders for now. requires margin from axis labels and/or title
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, (0,0,0), self.rect, width=1)

    def find_xgap(self):
        all_x = []
        for chart in self.charts:
            all_x += chart.x
        self.xmin = min(all_x)
        self.xmax = max(all_x)
        self.xgap = (self.width - 2 * self.chart_margin) / (self.xmax - self.xmin)

    def find_ymultiplier(self):
        all_y = []
        for chart in self.charts:
            all_y += chart.y
        self.ymin, self.ymax = min(all_y), max(all_y)
        self.ymultiplier = self.height / self.ymax # in chart drawing ymin = 0 by default

    def draw_line(self, chart):
        data = list(zip(chart.x, chart.y))
        data = [list(point) for point in data]

        for point in data:
            point[0] = (point[0] - self.xmin) * self.xgap
            point[1] = (self.ymax - point[1]) * self.ymultiplier
        
        x = self.x + self.chart_margin
        y = self.y
        for i in range(len(data) - 1):
            pygame.draw.line(self.figure.background, chart.color, 
                            (x + data[i][0], y + data[i][1]), 
                            (x + data[i+1][0], y + data[i+1][1]),
                            chart.line_width
                            )

    def draw_bar(self, chart):
        data = list(zip(chart.x, chart.y))
        data = [list(point) for point in data]

        for point in data:
            point[0] = (point[0] - self.xmin) * self.xgap
            point[1] = (self.ymax - point[1]) * self.ymultiplier
        
        x = self.x + self.chart_margin
        y = self.y
        for i in range(len(data)):
            pygame.draw.rect(self.figure.background, chart.color, 
                            pygame.Rect(x + data[i][0] - chart.bar_width/2, y + data[i][1], 
                                        chart.bar_width, self.height - data[i][1])
                            )


    def draw_all_charts(self):
        for chart in self.charts:
            if chart.__class__ == Line:
                self.draw_line(chart)
            elif chart.__class__ == Bar:
                self.draw_bar(chart)
            else:
                pass


class Line:
    def __init__(self, name, x, y, color, line_width): 
        self.name = name
        check = check_list_xy(x, y)
        if check:
            self.x = x
            self.y = y
        self.color = color
        self.line_width = line_width

class Bar:
    def __init__(self, name, x, y, color, bar_width):
        self.name = name
        check = check_list_xy(x, y)
        if check:
            self.x = x
            self.y = y
        self.color = color
        self.bar_width = bar_width


 

        

