import pygame, math
from settings import *
import util_functions as util


class Text:
    pygame.font.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    text_color = TEXT_COLOR

    def __init__(self, text, vertical=False):
        self.source_text = str(text)
        self.txt = self.font.render(self.source_text, True, self.text_color)
        if vertical:
            self.txt = pygame.transform.rotate(self.txt, 90)

    def write_fron_textOb(self, surface, position, center=True):
        txt_rect = self.txt.get_rect()
        if center:
            txt_rect.center = position
        else:
            txt_rect.topleft = position
        surface.blit(self.txt, txt_rect)



class Figure:
    def __init__(self,
                screen,
                x, y, width, height, # might implement an outer size (padding for the whole figure)
                bg_color = BG_COLOR,
                xlim = (None, None),
                ylim = (None, None),
                ):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.xlim = xlim
        self.ylim = ylim

        self.background = pygame.Surface((self.width, self.height))
        self.title = Title(self)
        self.legend = Legend(self)
        self.yaxis_label = yAxisLabel(self)
        self.xaxis_label = xAxisLabel(self)
        self.xaxis_tick = xAxisTick(self)
        self.yaxis_tick = yAxisTick(self)
        self.chart_area = ChartArea(self)

        self.xmin = self.xmax = None
        self.ymin = self.ymax = None

        self.chart_area.xdata_min = self.chart_area.xdata_max = None
        self.chart_area.ydata_min = self.chart_area.ydata_max = None

    def create_figure(self):
        self.screen.blit(self.background, (self.x, self.y))
        self.background.fill(self.bg_color)

    def set_xlim(self, xlim): # (xmin, xmax)
        if util.check_axis_limit(xlim):
            self.xmin = xlim[0]
            self.xmax = xlim[1]
            self.chart_area.xdata_type = 'numeric'
            
    def set_ylim(self, xlim): # (ymin, ymax)
        if util.check_axis_limit(ylim):
            self.ymin = ylim[0]
            self.ymax = ylim[1]

    def set_title(self, title):
        self.title.width = self.width
        self.title.x = 0
        self.title.y = 0
        self.title.adjust_inner_area()
        self.title.add_title(title)

    def set_legend(self):
        self.legend.width = self.width
        self.legend.x = 0
        self.legend.y = self.height - (self.legend.height)
        self.legend.adjust_inner_area()
        self.legend.add_legend()

    def set_yaxis_label(self):
        self.yaxis_label.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height)
        self.yaxis_label.x = 0
        self.yaxis_label.y = self.title.height
        self.yaxis_label.adjust_inner_area()
        self.yaxis_label.add_label()

    def set_xaxis_label(self):
        self.xaxis_label.width = self.width - self.yaxis_label.width
        self.xaxis_label.x = self.yaxis_label.width
        self.xaxis_label.y = self.height - (self.legend.height + self.xaxis_label.height)
        self.xaxis_label.adjust_inner_area()
        self.xaxis_label.add_label()

    def set_yaxis_tick(self):
        self.yaxis_tick.width = 20 # to be calculated later
        self.yaxis_tick.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.yaxis_tick.x = self.yaxis_label.width
        self.yaxis_tick.y = self.title.height

    def set_xaxis_tick(self):
        self.xaxis_tick.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width)
        self.xaxis_tick.height = 20 # to be calculated later
        self.xaxis_tick.x = self.yaxis_label.width + self.yaxis_tick.width
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)

    def set_chart_area(self):
        self.chart_area.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width)
        self.chart_area.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.chart_area.x = self.yaxis_label.width + self.yaxis_tick.width
        self.chart_area.y = self.title.height

    def line(self, name, xdata, ydata, color=None, line_width=1):
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area.add_chart(
            LineChart(name, xdata, ydata, color, line_width)
        )


    def draw(self):
        for area in [self.title, self.legend, self.yaxis_label, self.xaxis_label, self.yaxis_tick, self.xaxis_tick, self.chart_area]:
            area.draw()

    
class Area:
    def __init__(self, figure):
        self.figure = figure
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.innerx = 0
        self.innery = 0
        self.innerwidth = 0
        self.innerheight = 0

    def adjust_inner_area(self):
        self.innerx = self.x + PADDING
        self.innery = self.y + PADDING
        self.innerwidth = max(self.width - PADDING * 2, 0)
        self.innerheight = max(self.height - PADDING * 2, 0)

    def adjust_outer_area(self):
        self.x = max(self.innerx - PADDING, 0)
        self.y = max(self.innery - PADDING, 0)
        self.width = self.innerwidth + PADDING * 2
        self.height = self.innerheight + PADDING * 2

    def draw_area(self): # might be unnecessary, to be removed later
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, self.figure.bg_color, self.rect)

    def draw_area_border(self): # might be unnecessary, to be removed later
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, (0,0,0), self.rect, width=1)


class Title(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_title(self, title):
        self.txtOb = Text(title)
        self.innerheight = self.txtOb.txt.get_height()
        self.adjust_outer_area()
        self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)

    def draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)


class Legend(Area): # later to include true legend
    def __init__(self, figure):
        super().__init__(figure)

    def add_legend(self):
        self.txtOb = Text('LEGEND')
        self.innerheight = self.txtOb.txt.get_height()
        self.adjust_outer_area()
        self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)

    def draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)

class yAxisLabel(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_label(self):
        self.txtOb = Text('y-axis Label', True)
        self.innerwidth = self.txtOb.txt.get_width()
        self.adjust_outer_area()
        self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)

    def draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)

class xAxisLabel(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_label(self):
        self.txtOb = Text('x-axis Label', False)
        self.innerheight = self.txtOb.txt.get_height()
        self.adjust_outer_area()
        self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)

    def draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)

class xAxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.xmin = None
        self.xmax = None
    
    def calculate_ticks_string(self):
        self.ticks = []
        self.all_xdata = self.figure.chart_area.all_xdata
        startpos = self.figure.chart_area.x + self.figure.chart_area.chart_margin
        for i in range(len(self.all_xdata)):
            self.ticks.append([self.all_xdata[i], startpos + i * self.figure.chart_area.xdata_gap])

    def tick_range(self):
        data_span = self.xmax - self.xmin
        scale = 10 ** math.floor(math.log10(data_span))
        tick_size_normalized_list = [5.0, 2.0, 1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        tick_size_normalized = 1.0
        for i in range(len(tick_size_normalized_list)):
            num_tick = data_span / scale / tick_size_normalized_list[i]
            if num_tick > MAX_TICK:
                tick_size_normalized = tick_size_normalized_list[i-1]
                break
        tick_size = tick_size_normalized * scale
        ticks = util.create_range(self.xmin/tick_size, self.xmax/tick_size)
        return [i * tick_size for i in [round(i) for i in ticks]]

    def calculate_ticks_numeric(self): # should run before drawing charts
        if (self.figure.xmin != None) & (self.figure.xmax != None):
            self.xmin, self.xmax = self.figure.xmin, self.figure.xmax
            self.ticks = util.tick_range(self.xmin, self.xmax)
            self.ticks = [i for i in self.ticks if i>=self.xmin and i<=self.xmax]
        else:
            self.xmin, self.xmax = min(self.figure.chart_area.all_xdata), max(self.figure.chart_area.all_xdata)
            self.ticks = util.tick_range(self.xmin, self.xmax)
            self.xmin, self.xmax = min(self.ticks), max(self.ticks)

        startpos = self.figure.chart_area.x + self.figure.chart_area.chart_margin
        self.ticks = [[i, startpos + (i - self.xmin) * self.figure.chart_area.xdata_gap] for i in self.ticks]

    def write_ticks(self):
        for tick in self.ticks:
            tick_txtOb = Text(str(tick[0]))
            if tick_txtOb.txt.get_height() > self.height:
                self.height = tick_txtOb.txt.get_height()
            tick_txtOb.write_fron_textOb(self.figure.background, (tick[1], self.y + self.height / 2))

    def draw(self):
        self.draw_area()
        self.write_ticks()

class yAxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def draw(self):
        self.draw_area()
    
class ChartArea(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.charts = []
        self.chart_names = []
        self.chart_margin = 20 # should be optimized (padding on left and right)
        if self.figure.xlim != (None,None): ## error code for this should be different!!
            self.xdata_type = 'numeric'
        else:
            self.xdata_type = None

    def check_xdata(self, chart):
        if self.xdata_type:
            if self.xdata_type != chart.xdata_type:
                raise KeyError('All charts must have the same type for xdata!')
        else:
            self.xdata_type = chart.xdata_type

    def add_chart(self, chart):
        if chart.name not in self.chart_names:
            self.check_xdata(chart)
            self.charts.append(chart)
            self.chart_names.append(chart.name)
        else:
            self.update_chart(chart)

    def update_chart(self, chart):
        chart_to_update = [i for i in self.charts if i.name == chart.name][0]
        if chart_to_update is None:
            raise KeyError('No existing chart with the same name to update!')
        self.check_xdata(chart)
        chart_to_update.xdata = chart.xdata
        chart_to_update.ydata = chart.ydata

    def draw(self):
        self.draw_area_border()

    def combine_xdata(self):
        self.all_xdata = []
        for chart in self.charts:
            self.all_xdata += chart.xdata
        if self.xdata_type == 'str':
            self.all_xdata = list(set(self.all_xdata))
            self.all_xdata.sort()

    def find_xdata_gap_numeric(self):
        self.combine_xdata()
        # calcualte xmin/xmax for chart area. Hieararchy: figure level > xticks > xdata
        if (self.figure.xmin != None) & (self.figure.xmax != None):
            self.xdata_min, self.xdata_max = self.figure.xmin, self.figure.xmax
        elif (self.figure.xaxis_tick.xmin != None) & (self.figure.xaxis_tick.xmax != None):
            self.xdata_min, self.xdata_max = self.figure.xaxis_tick.xmin, self.figure.xaxis_tick.xmax
        else:
            self.xdata_min, self.xdata_max = min(self.all_xdata), max(self.all_xdata)

        self.xdata_gap = (self.width - 2 * self.chart_margin) / (self.xdata_max - self.xdata_min)

    def find_xdata_gap_string(self): # instead of set + sort, category names might be sorted acc to introduction of data
        self.combine_xdata()
        self.xdata_gap = (self.width - 2 * self.chart_margin) / (len(self.all_xdata) - 1)

    def find_ydata_multiplier(self):
        self.all_ydata = []
        for chart in self.charts:
            self.all_ydata += chart.ydata
        self.all_xdata = list(set(self.all_xdata))
        self.all_xdata.sort()
        if self.ydata_min == None: self.ydata_min = min(self.all_ydata)
        if self.ydata_max == None: self.ydata_max = max(self.all_ydata)
        self.ydata_multiplier = self.height / (self.ydata_max - self.ydata_min)

    def adjust_data_for_line(self, chart):
        data = list(zip(chart.xdata, chart.ydata))
        data = [list(point) for point in data]
        
        if self.xdata_type == 'numeric':
            data = [point for point in data if (point[0] >= self.xdata_min) & (point[0] <= self.xdata_max)]
            for point in data:
                point[0] = (point[0] - self.xdata_min) * self.xdata_gap
                point[1] = (self.ydata_max - point[1]) * self.ydata_multiplier
        else:
            for point in data:
                point[0] = self.all_xdata.index(point[0]) * self.xdata_gap
                point[1] = (self.ydata_max - point[1]) * self.ydata_multiplier
        
        return data


    def draw_line(self, chart):
        data = self.adjust_data_for_line(chart)

        x = self.x + self.chart_margin
        y = self.y
        for i in range(len(data) - 1):
            pygame.draw.line(
                self.figure.background,
                chart.color,
                (x + data[i][0], y + data[i][1]),
                (x + data[i+1][0], y + data[i+1][1]),
                chart.line_width
            )


    def draw_all_charts(self):
        if self.xdata_type == 'numeric':
            self.find_xdata_gap_numeric()
            self.figure.xaxis_tick.calculate_ticks_numeric()
        else:
            self.find_xdata_gap_string()
            self.figure.xaxis_tick.calculate_ticks_string()
        self.find_ydata_multiplier()

        for chart in self.charts:
            self.draw_line(chart)


class ChartType:
    def __init__(self, name, xdata, ydata, color):
        self.name = name
        check = util.check_xy_data(xdata, ydata)
        if check:
            self.xdata = xdata
            self.ydata = ydata
        if type(self.xdata[0]) in (int, float):
            self.xdata_type = 'numeric'
        else:
            self.xdata_type = 'str'
        self.color = color


class LineChart(ChartType):
    def __init__(self, name, xdata, ydata, color, line_width):
        super().__init__(name, xdata, ydata, color)
        self.line_width = line_width