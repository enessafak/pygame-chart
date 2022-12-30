import pygame, math, pygame.freetype
from settings import *
import util_functions as util


class TextFont:
    '''
    Text class, teking a string as argument and blit on any surface and position
    Utilizes pygame.font module. This class is saved as an alternative to default Text class using pygame.freetype module
    '''
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

class Text:
    '''
    Text class, teking a string as argument and blit on any surface and position
    Utilizes pygame.freetype module. This class is used in pygameChart as default
    '''
    pygame.freetype.init()
    font = pygame.freetype.SysFont(None, FONT_SIZE)
    text_color = TEXT_COLOR

    def __init__(self, text, vertical=False):
        self.source_text = str(text)
        self.txt, self.txt_rect = self.font.render(self.source_text, self.text_color)
        if vertical:
            self.txt = pygame.transform.rotate(self.txt, 90)
            self.txt_rect = self.txt.get_rect()

    def write_fron_textOb(self, surface, position, center=True):
        if center:
            self.txt_rect.center = position
        else:
            self.txt_rect.topleft = position
        surface.blit(self.txt, self.txt_rect)



class Figure:
    def __init__(self,
                screen,
                x, y, width, height, # might implement an outer size (padding for the whole figure)
                bg_color = BG_COLOR,
                ):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color

        # create surface for figure. all drawing is done on Figure.background
        self.background = pygame.Surface((self.width, self.height))
        # create instances for all figure areas
        self.title = Title(self)
        self.legend = Legend(self)
        self.yaxis_label = yAxisLabel(self)
        self.xaxis_label = xAxisLabel(self)
        self.xaxis_tick = xAxisTick(self)
        self.yaxis_tick = yAxisTick(self)
        self.chart_area = ChartArea(self)

        # set axis limits to None
        self.xmin = self.xmax = None
        self.ymin = self.ymax = None
        self.chart_area.xdata_min = self.chart_area.xdata_max = None
        self.chart_area.ydata_min = self.chart_area.ydata_max = None

    def create_figure(self):
        # blit figure background to screen
        self.screen.blit(self.background, (self.x, self.y))
        self.background.fill(self.bg_color)

    def set_xlim(self, xlim): 
        '''
        Sets xmin and xmax for all charts. Drawings out of these limits are unvisible
        xlim:   tuple(xmin, xmax)
        '''
        if util.check_axis_limit(xlim):
            self.xmin = xlim[0]
            self.xmax = xlim[1]
            self.chart_area.xdata_type = 'numeric'
            
    def set_ylim(self, ylim): 
        '''
        Sets ymin and ymax for all charts. Drawings out of these limits are unvisible
        ylim:   tuple(ymin, ymax)
        '''
        if util.check_axis_limit(ylim):
            self.ymin = ylim[0]
            self.ymax = ylim[1]

    def set_title(self, title):
        '''
        Sets figure title to be shown at the top, center aligned.
        title:  str
        '''
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

    def set_yaxis_label(self, label):
        '''
        Sets axis label for y-axis.
        label:  str
        '''
        self.yaxis_label.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height)
        self.yaxis_label.x = 0
        self.yaxis_label.y = self.title.height
        self.yaxis_label.adjust_inner_area()
        self.yaxis_label.add_label(label)

    def set_xaxis_label(self, label):
        '''
        Sets axis label for x-axis.
        label:  str
        '''
        self.xaxis_label.width = self.width - self.yaxis_label.width
        self.xaxis_label.x = self.yaxis_label.width
        self.xaxis_label.y = self.height - (self.legend.height + self.xaxis_label.height)
        self.xaxis_label.adjust_inner_area()
        self.xaxis_label.add_label(label)

    def set_yaxis_tick(self):
        # set y-tick size and position. initial width is set 0, to be calculated later according to tick text width
        self.yaxis_tick.width = 0 
        self.yaxis_tick.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.yaxis_tick.x = self.yaxis_label.width
        self.yaxis_tick.y = self.title.height

    def set_xaxis_tick(self):
        # set x-tick size and position. initial height is set 0, to be calculated later according to tick text height
        self.xaxis_tick.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width)
        self.xaxis_tick.height = 0 
        self.xaxis_tick.x = self.yaxis_label.width + self.yaxis_tick.width
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)

    def set_chart_area(self):
        # set chart area size and position. chart area fills entire space left from other Area objects
        self.chart_area.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width) - PADDING
        self.chart_area.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.chart_area.x = self.yaxis_label.width + self.yaxis_tick.width
        self.chart_area.y = self.title.height

    def line(self, name, xdata, ydata, color=None, line_width=2):
        '''
        Adds line chart to the figure.
        name:       Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must be added with
                    a unique name. If another chart is provided whith the same name, the data updated
        xdata:      list (all number or all string)
        ydata:      list (all number)
        color:      (RGB values)
        line_width: width of the line chart
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area.add_chart(
            LineChart(name, xdata, ydata, color, line_width)
        )

    def bar(self, name, xdata, ydata, color=None, bar_width=None):
        '''
        Adds bar chart to the figure.
        name:       Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must be added with
                    a unique name. If another chart is provided whith the same name, the data updated
        xdata:      list (all number or all string)
        ydata:      list (all number)
        color:      (RGB values)
        bar_width:  width of the bar chart
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area.add_chart(
            BarChart(name, xdata, ydata, color, bar_width)
        )

    def scatter(self, name, xdata, ydata, color=None, radius=3):
        '''
        Adds scatter chart to the figure.
        name:   Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must be added with
                a unique name. If another chart is provided whith the same name, the data updated
        xdata:  list (all number or all string)
        ydata:  list (all number)
        color:  (RGB values)
        radius: radius of the marker
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area.add_chart(
            ScatterChart(name, xdata, ydata, color, radius)
        )

    def draw(self):
        '''
        Draws the figure with setted areas and charts provided
        '''        

        self.chart_area.combine_data()

        self.set_yaxis_tick()
        self.yaxis_tick.calculate_ticks()
        self.yaxis_tick.calculate_width()

        self.set_xaxis_tick()
        self.xaxis_tick.calculate_ticks()
        self.xaxis_tick.calculate_height()
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)

        self.set_chart_area()
        self.chart_area.draw_all_charts()
        self.chart_area.draw()

        self.title.draw()
        self.legend.draw()
        self.yaxis_label.draw()
        self.xaxis_label.draw()
        self.yaxis_tick.draw()
        self.xaxis_tick.draw()


    
class Area:
    '''
    Base object for figure areas: title, legend, x-y axis labels, x-y axis ticks and chart area
    '''
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
        # in order to provide a padding for the area, there are inner and outer areas. this method adjusts inner area acc to outer area
        self.innerx = self.x + PADDING
        self.innery = self.y + PADDING
        self.innerwidth = max(self.width - PADDING * 2, 0)
        self.innerheight = max(self.height - PADDING * 2, 0)

    def adjust_outer_area(self):
        # in order to provide a padding for the area, there are inner and outer areas. this method adjusts outer area acc to inner area
        self.x = max(self.innerx - PADDING, 0)
        self.y = max(self.innery - PADDING, 0)
        self.width = self.innerwidth + PADDING * 2
        self.height = self.innerheight + PADDING * 2

    def draw_area(self):
        # draw the area with the same background color of figure. useful for hiding chart drawings out of figure data limits
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.figure.background, self.figure.bg_color, self.rect)

    def draw_area_border(self): 
        # draw the area with border and no fill color
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

    def add_label(self, label):
        self.txtOb = Text(label, True)
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

    def add_label(self, label):
        self.txtOb = Text(label, False)
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
        # calculates string vars from all charts
        self.ticks = self.figure.chart_area.all_xdata
    
    def calculate_ticks_numeric(self): 
        # calculates ticks according to figure limit or provided chart data
        if (self.figure.xmin != None) & (self.figure.xmax != None):
            # if xlim is set on figure level, use these boundaries in tick calculation. later remove any tick outside figure limit
            self.xmin, self.xmax = self.figure.xmin, self.figure.xmax
            self.ticks = util.tick_range(self.xmin, self.xmax)
            self.ticks = [i for i in self.ticks if i>=self.xmin and i<=self.xmax]
        else:
            # if no xlim is set on figure level, use min/max values from charts.
            self.xmin, self.xmax = min(self.figure.chart_area.all_xdata), max(self.figure.chart_area.all_xdata)
            self.ticks = util.tick_range(self.xmin, self.xmax)
            self.xmin, self.xmax = min(self.ticks), max(self.ticks)

    def calculate_ticks(self):
        if self.figure.chart_area.xdata_type == 'str':
            self.calculate_ticks_string()
        else:
            self.calculate_ticks_numeric()

    def calculate_height(self):
        # max height of tick text objects
        txtObs = [Text(str(i)) for i in self.ticks]
        txtObs_heights = [i.txt.get_height() for i in txtObs]
        self.height = max(txtObs_heights) + PADDING

    def write_ticks(self):
        # first get start position from chart area. then adjust ticks list as [tick, position]
        if self.figure.chart_area.xdata_type == 'numeric':
            startpos = self.figure.chart_area.x + self.figure.chart_area.chart_margin
            self.ticks = [[i, startpos + (i - self.xmin) * self.figure.chart_area.xdata_gap] for i in self.ticks]
        else:
            startpos = self.figure.chart_area.x + self.figure.chart_area.chart_margin
            for i in range(len(self.ticks)):
                self.ticks[i] = [self.ticks[i], startpos + i * self.figure.chart_area.xdata_gap]

        # for each [tick, position] couple create a Text object and write center-aligned
        for tick in self.ticks:
            tick_txtOb = Text(str(tick[0]))
            tick_txtOb.write_fron_textOb(self.figure.background, (tick[1], self.y + self.height / 2))


    def draw(self):
        self.draw_area()
        self.write_ticks()

class yAxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.ymin = None
        self.ymax = None

    def calculate_ticks(self): # should run before drawing charts
        # calculates ticks according to figure limit or provided chart data
        if (self.figure.ymin != None) & (self.figure.ymax != None):
            # if ylim is set on figure level, use these boundaries in tick calculation. later remove any tick outside figure limit
            self.ymin, self.ymax = self.figure.ymin, self.figure.ymax
            self.ticks = util.tick_range(self.ymin, self.ymax)
            self.ticks = [i for i in self.ticks if i>=self.ymin and i<=self.ymax]
        else:
            # if no ylim is set on figure level, use min/max values from charts.
            self.ymin, self.ymax = min(self.figure.chart_area.all_ydata), max(self.figure.chart_area.all_ydata)
            self.ticks = util.tick_range(self.ymin, self.ymax)
            self.ymin, self.ymax = min(self.ticks), max(self.ticks)

    def calculate_width(self):
        # max width of tick text objects
        txtObs = [Text(str(i)) for i in self.ticks]
        txtObs_widths = [i.txt.get_width() for i in txtObs]
        self.width = max(txtObs_widths) + PADDING
    
    def write_ticks(self):
        # first get start position from chart area. then adjust ticks list as [tick, position]
        startpos = self.figure.chart_area.y
        self.ticks = [[i, startpos + (self.ymax - i) * self.figure.chart_area.ydata_multiplier] for i in self.ticks]

        # for each [tick, position] couple create a Text object and write center-aligned
        for tick in self.ticks:
            tick_txtOb = Text(str(tick[0]))
            tick_txtOb.write_fron_textOb(self.figure.background, (self.x + self.width / 2, tick[1]))

    def draw(self):
        self.draw_area()
        self.write_ticks()
    
class ChartArea(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.charts = []
        self.chart_names = []
        self.chart_margin = PADDING
        self.xdata_type = None

    def check_xdata(self, chart):
        # checks if provided xdata is aligned with previously provided charts. cannot draw multiple charts with one numberic and one string
        # xdata. also, if figure.xlim is porvided (must be number) no categoric data can be drawn
        if self.xdata_type:
            if self.xdata_type != chart.xdata_type:
                raise KeyError('All charts must have the same type for xdata!')
        else:
            self.xdata_type = chart.xdata_type

    def add_chart(self, chart):
        # chart object can be any extension of ChartType object. chart-name is handy here since just appending charts create abundance of
        # duplicates in game loop. therefore, in each step, checks if the chart already exists. if so, updates chart
        if chart.name not in self.chart_names:
            self.check_xdata(chart)
            self.charts.append(chart)
            self.chart_names.append(chart.name)
        else:
            self.update_chart(chart)

    def update_chart(self, chart):
        # find the chart over unique name and update xdata and ydata
        chart_to_update = [i for i in self.charts if i.name == chart.name][0]
        if chart_to_update is None:
            raise KeyError('No existing chart with the same name to update!')
        self.check_xdata(chart)
        chart_to_update.xdata = chart.xdata
        chart_to_update.ydata = chart.ydata

    def draw(self):
        self.draw_area_border()

    def combine_xdata(self):
        # combines all xdata from all charts
        self.all_xdata = []
        for chart in self.charts:
            self.all_xdata += chart.xdata
        if self.xdata_type == 'str':
            self.all_xdata = list(set(self.all_xdata))
            self.all_xdata.sort()

    def combine_ydata(self):
        # combines all ydata from all charts
        self.all_ydata = []
        for chart in self.charts:
            self.all_ydata += chart.ydata
        self.all_ydata = list(set(self.all_ydata))
        self.all_ydata.sort()

    def combine_data(self):
        self.combine_xdata()
        self.combine_ydata()

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
        # calcualte ymin/ymax for chart area. Hieararchy: figure level > yticks > ydata
        if (self.figure.ymin != None) & (self.figure.ymax != None):
            self.ydata_min, self.ydata_max = self.figure.ymin, self.figure.ymax
        elif (self.figure.yaxis_tick.ymin != None) & (self.figure.yaxis_tick.ymax != None):
            self.ydata_min, self.ydata_max = self.figure.yaxis_tick.ymin, self.figure.yaxis_tick.ymax
        else:
            self.ydata_min, self.ydata_max = min(self.all_ydata), max(self.all_ydata)

        self.ydata_multiplier = self.height / (self.ydata_max - self.ydata_min)

    def adjust_data_for_line_scatter(self, chart):
        # data is a list of tuples for xdata and ydata
        data = list(zip(chart.xdata, chart.ydata))
        data = [list(point) for point in data]
        
        if self.xdata_type == 'numeric':
            # remove points outside of x-axis boundaries. if figure.xlim is set, self.xdata_min/max = figure.xmin/max
            data = [point for point in data if (point[0] >= self.xdata_min) & (point[0] <= self.xdata_max)]
            for point in data:
                point[0] = (point[0] - self.xdata_min) * self.xdata_gap
                # distance of end point to top of the chart (ydata_max)
                point[1] = (self.ydata_max - point[1]) * self.ydata_multiplier
        else:
            for point in data:
                point[0] = self.all_xdata.index(point[0]) * self.xdata_gap
                # distance of end point to top of the chart (ydata_max)
                point[1] = (self.ydata_max - point[1]) * self.ydata_multiplier
        
        return data


    def draw_line(self, chart):
        data = self.adjust_data_for_line_scatter(chart)

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

    def draw_scatter(self, chart):
        data = self.adjust_data_for_line_scatter(chart)
        x = self.x + self.chart_margin
        y = self.y
        for i in range(len(data)):
            pygame.draw.circle(
                self.figure.background, 
                chart.color, 
                (x + data[i][0], y + data[i][1]), 
                chart.radius
                )

    def adjust_data_for_bar(self, chart):
        data = list(zip(chart.xdata, chart.ydata))
        data = [list(point) for point in data]

        if self.xdata_type == 'numeric':
            # remove points outside of x-axis boundaries. if figure.xlim is set, self.xdata_min/max = figure.xmin/max
            data = [point for point in data if (point[0] >= self.xdata_min) & (point[0] <= self.xdata_max)]
            for point in data:
                point[0] = (point[0] - self.xdata_min) * self.xdata_gap
                # height of the bar (includes negative values)
                point[1] = point[1] * self.ydata_multiplier
        else:
            for point in data:
                point[0] = self.all_xdata.index(point[0]) * self.xdata_gap
                # height of the bar (includes negative values)
                point[1] = point[1] * self.ydata_multiplier
        
        return data

    def draw_bar(self, chart):
        data = self.adjust_data_for_bar(chart)

        x = self.x + self.chart_margin
        y = self.y + self.ydata_max * self.ydata_multiplier # position of 0 on y-axis
        if chart.bar_width == None:
            chart.bar_width = self.xdata_gap/3*2

        for i in range(len(data)):
            pygame.draw.rect(
                self.figure.background, 
                chart.color, 
                pygame.Rect(
                    x + data[i][0] - chart.bar_width / 2, 
                    y - data[i][1] if data[i][1]>=0 else y, # start from data above 0-point for positive values, at 0-point for negative values
                    chart.bar_width, 
                    abs(data[i][1]) # handle both positive and negative values
                    )
            )

    def draw_all_charts(self):
        if self.xdata_type == 'numeric':
            self.find_xdata_gap_numeric()
        else:
            self.find_xdata_gap_string()
        self.find_ydata_multiplier()

        for chart in self.charts:
            if chart.__class__ == LineChart:
                self.draw_line(chart)
            elif chart.__class__ == BarChart:
                self.draw_bar(chart)
            elif chart.__class__ == ScatterChart:
                self.draw_scatter(chart)
            else:
                pass


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

class BarChart(ChartType):
    def __init__(self, name, xdata, ydata, color, bar_width):
        super().__init__(name, xdata, ydata, color)
        self.bar_width = bar_width

class ScatterChart(ChartType):
    def __init__(self, name, xdata, ydata, color, radius):
        super().__init__(name, xdata, ydata, color)
        self.radius = radius