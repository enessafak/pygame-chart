import pygame, math, pygame.freetype
from settings import *
import util_functions as util


class TextFont:
    '''
    Text class, teking a string as argument and blit on any surface and position
    Utilizes pygame.font module. This class is saved as an alternative to default Text class using pygame.freetype module
    '''
    pygame.font.init()
    

    def __init__(self, text, vertical=False, font_size=FONT_SIZE, text_color=TEXT_COLOR):
        self.font = pygame.font.SysFont(None, font_size)
        self.text_color = TEXT_COLOR
        self.source_text = str(text)
        self.txt = self.font.render(self.source_text, True, self.text_color)
        if vertical:
            self.txt = pygame.transform.rotate(self.txt, 90)

    def write_fron_textOb(self, surface, position, align='center'): # align in ['center','topleft','center_vertical']
        txt_rect = self.txt.get_rect()
        if align == 'center':
            txt_rect.center = position
        elif align == 'topleft':
            txt_rect.topleft = position
        elif align == 'center_vertical':
            txt_rect.left = position[0]
            txt_rect.centery = position[1]
        surface.blit(self.txt, txt_rect)


class Text:
    '''
    Text class, teking a string as argument and blit on any surface and position
    Utilizes pygame.freetype module. This class is used in pygameChart as default.
    text:       string      Text to be written
    vertical:   boolean     True if the text is rotated clockwise for 90 degree
    font_size:  number      Default = 12 in settings.py
    text_color: RGB tuple   Default = (0,0,0) in settings.py
    '''
    pygame.freetype.init()

    def __init__(self, text, vertical=False, font_size=FONT_SIZE, text_color=TEXT_COLOR):
        self.font = pygame.freetype.SysFont(None, font_size)
        self.text_color = text_color
        self.source_text = str(text)
        self.txt, self.txt_rect = self.font.render(self.source_text, self.text_color)
        if vertical:
            self.txt = pygame.transform.rotate(self.txt, 90)
            self.txt_rect = self.txt.get_rect()

    def write_fron_textOb(self, surface, position, align='center'): # align in ['center','topleft','center_vertical']
        if align == 'center':
            self.txt_rect.center = position
        elif align == 'topleft':
            self.txt_rect.topleft = position
        elif align == 'center_vertical':
            self.txt_rect.left = position[0]
            self.txt_rect.centery = position[1]
        surface.blit(self.txt, self.txt_rect)



class Figure:
    '''
    Main figure object initiated with
    screen:     pygame.display  Main display the figure is drawn
    x,y:        number          Position of topleft corner of the figure in the screen
    width:      number          Width of the figure
    height:     number          Height of the figure
    bg_color:   RGB tuple       Default = (255,255,255) in settings.py
    '''
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

    def _create_figure(self):
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

    def add_title(self, title):
        '''
        Adds chart title at the top of the figure
        title:   str
        '''
        self.title.add_title(title)
        self.title.show = 1

    def add_legend(self):
        '''
        Adds legend at the bottom of the figure
        '''
        self.legend.show = 1

    def add_yaxis_label(self, label):
        '''
        Sets axis label for y-axis.
        label:  str
        '''
        self.yaxis_label.add_label(label)
        self.yaxis_label.show = 1

    def add_xaxis_label(self, label):
        '''
        Sets axis label for x-axis.
        label:  str
        '''
        self.xaxis_label.add_label(label)
        self.xaxis_label.show = 1

    def add_gridlines(self):
        '''
        Add both vertical and horizontal gridlines
        '''
        self.chart_area.gridlines = 1

    def _set_yaxis_tick(self):
        # set y-tick size and position. initial width is set 0, to be calculated later according to tick text width
        self.yaxis_tick.width = 0 
        self.yaxis_tick.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.yaxis_tick.x = self.yaxis_label.width
        self.yaxis_tick.y = self.title.height
        self.yaxis_tick.show = 1

    def _set_xaxis_tick(self):
        # set x-tick size and position. initial height is set 0, to be calculated later according to tick text height
        self.xaxis_tick.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width)
        self.xaxis_tick.height = 0 
        self.xaxis_tick.x = self.yaxis_label.width + self.yaxis_tick.width
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.xaxis_tick.show = 1

    def _set_chart_area(self):
        # set chart area size and position. chart area fills entire space left from other Area objects
        self.chart_area.width = self.width - (self.yaxis_label.width + self.yaxis_tick.width) - PADDING
        self.chart_area.height = self.height - (self.title.height + self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)
        self.chart_area.x = self.yaxis_label.width + self.yaxis_tick.width
        self.chart_area.y = self.title.height
        self.chart_area.show = 1

    def line(self, name, xdata, ydata, color=None, line_width=2):
        '''
        Adds line chart to the figure.
        name:       str     Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must 
                            be added with a unique name. If another chart is provided whith the same name, the data updated
        xdata:      list    all numbers or all string
        ydata:      list    all numbers
        color:      RGB tuple
        line_width: number  width of the line chart
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area._add_chart(
            LineChart(name, xdata, ydata, color, line_width)
        )

    def bar(self, name, xdata, ydata, color=None, bar_width=None):
        '''
        Adds bar chart to the figure.
        name:       str     Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must 
                            be added with a unique name. If another chart is provided whith the same name, the data updated
        xdata:      list    all numbers or all string
        ydata:      list    all numbers
        color:      RGB tuple
        bar_width:  number  width of the bar chart
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area._add_chart(
            BarChart(name, xdata, ydata, color, bar_width)
        )

    def scatter(self, name, xdata, ydata, color=None, radius=3):
        '''
        Adds scatter chart to the figure.
        name:       str     Name of the chart. Naming charts is necessary to keep track of charts in game loop. Each different chart must 
                            be added with a unique name. If another chart is provided whith the same name, the data updated
        xdata:      list    all numbers or all string
        ydata:      list    all numbers
        color:      RGB tuple
        radius:     number  radius of the marker
        '''
        if color == None:
            i = len(self.chart_area.charts)
            color = COLORS[i%len(COLORS)]

        self.chart_area._add_chart(
            ScatterChart(name, xdata, ydata, color, radius)
        )

    def _set_filler(self, x, y, width, height):
        # adds a filler area to the empty space left in corner of x-y label areas and x-y tick areas
        filler = Area(self)
        filler.x = x
        filler.y = y
        filler.width = width
        filler.height = height
        filler.show = 1
        filler.draw_area()

    def draw(self):
        '''
        Draws the figure with setted areas and charts provided. Final method to show the figure
        '''    
        self._create_figure()

        # adjustments for size and position of Areas
        self.title._adjust_size_pos()
        self.legend._adjust_size_pos()
        self.yaxis_label._adjust_size_pos()
        self.xaxis_label._adjust_size_pos()

        # chart area and ticks
        self.chart_area._combine_data()

        self._set_yaxis_tick()
        self.yaxis_tick._calculate_ticks()
        self.yaxis_tick._calculate_width()

        self._set_xaxis_tick()
        self.xaxis_tick._calculate_ticks()
        self.xaxis_tick._calculate_height()
        self.xaxis_tick.y = self.height - (self.legend.height + self.xaxis_label.height + self.xaxis_tick.height)

        self._set_chart_area()
        self.chart_area._find_xdata_gap_ydata_multiplier()
        self.chart_area._draw_gridlines()
        self.chart_area._draw_all_charts()
        self.chart_area._draw()

        # drawing
        self._set_filler(0, self.chart_area.y + self.chart_area.height, self.width, self.height - (self.chart_area.y + self.chart_area.height))
        self._set_filler(self.width - PADDING, self.chart_area.y, PADDING, self.chart_area.height)
        self._set_filler(0, self.chart_area.y, self.chart_area.x, self.chart_area.height)
        self.title._draw()
        self.legend._draw()
        self.yaxis_label._draw()
        self.xaxis_label._draw()
        self.yaxis_tick._draw()
        self.xaxis_tick._draw()


    
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
        self.show = 0

    def _adjust_inner_area(self):
        # in order to provide a padding for the area, there are inner and outer areas. this method adjusts inner area acc to outer area
        self.innerx = self.x + PADDING
        self.innery = self.y + PADDING
        self.innerwidth = max(self.width - PADDING * 2, 0)
        self.innerheight = max(self.height - PADDING * 2, 0)

    def _adjust_outer_area(self):
        # in order to provide a padding for the area, there are inner and outer areas. this method adjusts outer area acc to inner area
        self.x = max(self.innerx - PADDING, 0)
        self.y = max(self.innery - PADDING, 0)
        self.width = self.innerwidth + PADDING * 2
        self.height = self.innerheight + PADDING * 2

    def draw_area(self):
        # draw the area with the same background color of figure. useful for hiding chart drawings out of figure data limits
        if self.show:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(self.figure.background, self.figure.bg_color, self.rect)

    def draw_area_border(self): 
        # draw the area with border and no fill color
        if self.show:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(self.figure.background, (0,0,0), self.rect, width=1)




class Title(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_title(self, title):
        self.txtOb = Text(title, font_size=TITLE_FONT_SIZE)
        self.txtOb.font
        self.innerheight = self.txtOb.txt.get_height()
        
    def _adjust_size_pos(self):
        self.width = self.figure.width
        self.x = 0
        self.y = 0
        self.height = self.innerheight + PADDING * 2
        self._adjust_inner_area()

    def _draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)



class Legend(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.line_height = MIN_LEGEND_LINE_HEIGHT
        self.item_width = LEGEND_ITEM_WIDTH

    def _calculate_line_width_height(self):
        self.width = self.figure.width
        self.innerwidth = self.width - 2 * PADDING

        charts = self.figure.chart_area.chart_names
        charts = [Text(chart) for chart in charts]
        self.lines = []
        width = 0
        line = 1
        for chart in charts:
            self.line_height = max(self.line_height, chart.txt.get_height())
            name_w = self.item_width + PADDING + chart.txt.get_width() + PADDING # chart item + padding + chart name + padding
            if width + name_w > self.innerwidth: 
                line += 1
                self.lines.append(width)
                width = name_w
            else:
                width += name_w
        self.lines.append(width)

    def _adjust_size_pos(self):
        self._calculate_line_width_height()
        self.innerwidth = max(self.lines)
        self.innerheight = self.line_height * len(self.lines)
        self.innerx = (self.figure.width - self.innerwidth) / 2
        self.innery = self.figure.height - (self.innerheight + PADDING)
        self._adjust_outer_area()

    def _write_legend_items(self):
        charts = self.figure.chart_area.charts
        i = 0
        y = self.innery
        for line_width in self.lines:
            width = 0
            x = self.innerx
            while width < line_width:
                chart = charts[i]
                self._draw_legend_item(chart, (x+ width, y))
                width += self.item_width + PADDING
                width_inc = self._write_chart_name(chart, (x + width, y + self.line_height / 2))
                width += width_inc + PADDING
                i += 1   
            y += self.line_height
                
    def _draw_legend_item(self, chart, pos):
        if chart.__class__ == LineChart:
            linepos = (pos[0], pos[1] + self.line_height / 2)
            pygame.draw.aaline(self.figure.background, chart.color, linepos, (linepos[0] + self.item_width, linepos[1]))
        elif chart.__class__ == BarChart:
            pygame.draw.rect(self.figure.background, chart.color, pygame.Rect(pos[0], pos[1], self.item_width, self.line_height))
        elif chart.__class__ == ScatterChart:
            pygame.draw.circle(self.figure.background, chart.color, (pos[0] + self.item_width / 2, pos[1] + self.line_height / 2), 3)


    def _write_chart_name(self, chart, pos):
        txt = Text(chart.name)
        txt.write_fron_textOb(self.figure.background, pos, 'center_vertical')
        return txt.txt.get_width()


    def _draw(self):
        if self.show:
            self.draw_area()
            self.draw_area_border()
            self._write_legend_items()

class yAxisLabel(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_label(self, label):
        self.txtOb = Text(label, True)
        self.innerwidth = self.txtOb.txt.get_width()

    def _adjust_size_pos(self):
        self.height = self.figure.height - (self.figure.title.height + self.figure.legend.height + self.figure.xaxis_label.height)
        self.x = 0
        self.y = self.figure.title.height
        self.width = self.innerwidth + PADDING * 2
        self._adjust_inner_area()

    def _draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)

class xAxisLabel(Area):
    def __init__(self, figure):
        super().__init__(figure)

    def add_label(self, label):
        self.txtOb = Text(label, False)
        self.innerheight = self.txtOb.txt.get_height()

    def _adjust_size_pos(self):
        self.width = self.figure.width - self.figure.yaxis_label.width
        self.height = self.innerheight + PADDING * 2
        self.x = self.figure.yaxis_label.width
        self.y = self.figure.height - (self.figure.legend.height + self.height)
        self._adjust_inner_area()

    def _draw(self):
        self.draw_area()
        if 'txtOb' in dir(self):
            self.txt_position = (self.x + self.width / 2, self.y + self.height / 2)
            self.txtOb.write_fron_textOb(self.figure.background, self.txt_position)

class xAxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.xmin = None
        self.xmax = None
    
    def _calculate_ticks_string(self):
        # calculates string vars from all charts
        self.ticks = self.figure.chart_area.all_xdata
    
    def _calculate_ticks_numeric(self): 
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

    def _calculate_ticks(self):
        if self.figure.chart_area.xdata_type == 'str':
            self._calculate_ticks_string()
        else:
            self._calculate_ticks_numeric()

    def _calculate_height(self):
        # max height of tick text objects
        txtObs = [Text(str(i)) for i in self.ticks]
        txtObs_heights = [i.txt.get_height() for i in txtObs]
        self.height = max(txtObs_heights) + PADDING

    def _write_ticks(self):
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


    def _draw(self):
        self.draw_area()
        self._write_ticks()

class yAxisTick(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.ymin = None
        self.ymax = None

    def _calculate_ticks(self): # should run before drawing charts
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

    def _calculate_width(self):
        # max width of tick text objects
        txtObs = [Text(str(i)) for i in self.ticks]
        txtObs_widths = [i.txt.get_width() for i in txtObs]
        self.width = max(txtObs_widths) + PADDING
    
    def _write_ticks(self):
        # first get start position from chart area. then adjust ticks list as [tick, position]
        startpos = self.figure.chart_area.y + self.figure.chart_area.chart_margin
        self.ticks = [[i, startpos + (self.ymax - i) * self.figure.chart_area.ydata_multiplier] for i in self.ticks]

        # for each [tick, position] couple create a Text object and write center-aligned
        for tick in self.ticks:
            tick_txtOb = Text(str(tick[0]))
            tick_txtOb.write_fron_textOb(self.figure.background, (self.x + self.width / 2, tick[1]))

    def _draw(self):
        self.draw_area()
        self._write_ticks()
    
class ChartArea(Area):
    def __init__(self, figure):
        super().__init__(figure)
        self.charts = []
        self.chart_names = []
        self.chart_margin = CHART_MARGIN
        self.xdata_type = None
        self.gridlines = 0

    def _check_xdata(self, chart):
        # checks if provided xdata is aligned with previously provided charts. cannot draw multiple charts with one numberic and one string
        # xdata. also, if figure.xlim is porvided (must be number) no categoric data can be drawn
        if self.xdata_type:
            if self.xdata_type != chart.xdata_type:
                raise KeyError('All charts must have the same type for xdata!')
        else:
            self.xdata_type = chart.xdata_type

    def _add_chart(self, chart):
        # chart object can be any extension of ChartType object. chart-name is handy here since just appending charts create abundance of
        # duplicates in game loop. therefore, in each step, checks if the chart already exists. if so, updates chart
        if chart.name not in self.chart_names:
            self._check_xdata(chart)
            self.charts.append(chart)
            self.chart_names.append(chart.name)
        else:
            self._update_chart(chart)

    def _update_chart(self, chart):
        # find the chart over unique name and update xdata and ydata
        chart_to_update = [i for i in self.charts if i.name == chart.name][0]
        if chart_to_update is None:
            raise KeyError('No existing chart with the same name to update!')
        self._check_xdata(chart)
        chart_to_update.xdata = chart.xdata
        chart_to_update.ydata = chart.ydata

    def _draw(self):
        self.draw_area_border()

    def _combine_xdata(self):
        # combines all xdata from all charts
        self.all_xdata = []
        for chart in self.charts:
            self.all_xdata += chart.xdata
        if self.xdata_type == 'str':
            self.all_xdata = list(set(self.all_xdata))
            self.all_xdata.sort()

    def _combine_ydata(self):
        # combines all ydata from all charts
        self.all_ydata = []
        for chart in self.charts:
            self.all_ydata += chart.ydata
        self.all_ydata = list(set(self.all_ydata))
        self.all_ydata.sort()

    def _combine_data(self):
        self._combine_xdata()
        self._combine_ydata()

    def _find_xdata_gap_numeric(self):
        self._combine_xdata()
        # calcualte xmin/xmax for chart area. Hieararchy: figure level > xticks > xdata
        if (self.figure.xmin != None) & (self.figure.xmax != None):
            self.xdata_min, self.xdata_max = self.figure.xmin, self.figure.xmax
        elif (self.figure.xaxis_tick.xmin != None) & (self.figure.xaxis_tick.xmax != None):
            self.xdata_min, self.xdata_max = self.figure.xaxis_tick.xmin, self.figure.xaxis_tick.xmax
        else:
            self.xdata_min, self.xdata_max = min(self.all_xdata), max(self.all_xdata)

        self.xdata_gap = (self.width - 2 * self.chart_margin) / (self.xdata_max - self.xdata_min)

    def _find_xdata_gap_string(self): # instead of set + sort, category names might be sorted acc to introduction of data
        self._combine_xdata()
        self.xdata_gap = (self.width - 2 * self.chart_margin) / (len(self.all_xdata) - 1)

    def _find_ydata_multiplier(self):
        # calcualte ymin/ymax for chart area. Hieararchy: figure level > yticks > ydata
        if (self.figure.ymin != None) & (self.figure.ymax != None):
            self.ydata_min, self.ydata_max = self.figure.ymin, self.figure.ymax
        elif (self.figure.yaxis_tick.ymin != None) & (self.figure.yaxis_tick.ymax != None):
            self.ydata_min, self.ydata_max = self.figure.yaxis_tick.ymin, self.figure.yaxis_tick.ymax
        else:
            self.ydata_min, self.ydata_max = min(self.all_ydata), max(self.all_ydata)

        self.ydata_multiplier = (self.height - 2 * self.chart_margin) / (self.ydata_max - self.ydata_min)

    def _find_xdata_gap_ydata_multiplier(self):
        if self.xdata_type == 'numeric':
            self._find_xdata_gap_numeric()
        else:
            self._find_xdata_gap_string()
        self._find_ydata_multiplier()

    def _adjust_data_for_line_scatter(self, chart):
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


    def _draw_line(self, chart):
        data = self._adjust_data_for_line_scatter(chart)

        x = self.x + self.chart_margin
        y = self.y + self.chart_margin
        for i in range(len(data) - 1):
            pygame.draw.aaline(
                self.figure.background,
                chart.color,
                (x + data[i][0], y + data[i][1]),
                (x + data[i+1][0], y + data[i+1][1]),
                chart.line_width
            )

    def _draw_scatter(self, chart):
        data = self._adjust_data_for_line_scatter(chart)
        x = self.x + self.chart_margin
        y = self.y + self.chart_margin
        for i in range(len(data)):
            pygame.draw.circle(
                self.figure.background, 
                chart.color, 
                (x + data[i][0], y + data[i][1]), 
                chart.radius
                )

    def _adjust_data_for_bar(self, chart):
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

    def _draw_bar(self, chart):
        data = self._adjust_data_for_bar(chart)

        x = self.x + self.chart_margin
        y = self.y + self.chart_margin + self.ydata_max * self.ydata_multiplier # position of 0 on y-axis
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
                    abs(data[i][1]) + 1 # handle both positive and negative values
                    )
            )


    def _get_certain_chart_type(self, chart_type):
        return [chart for chart in self.charts if chart.__class__.__name__ == chart_type]


    def _draw_all_charts(self):
        # drawing order: bar, line, scatter
        # this is not to make latter invisible after the former chart type
        charts = []
        for chart_type in ['BarChart','LineChart','ScatterChart']:
            charts += self._get_certain_chart_type(chart_type)

        for chart in charts:
            if chart.__class__ == LineChart:
                self._draw_line(chart)
            elif chart.__class__ == BarChart:
                self._draw_bar(chart)
            elif chart.__class__ == ScatterChart:
                self._draw_scatter(chart)
            else:
                pass

    def _draw_vertical_gridlines(self):
        ticks = self.figure.xaxis_tick.ticks
        startpos = self.x + self.chart_margin
        if self.xdata_type == 'numeric':
            ticks = [startpos + (i - self.figure.xaxis_tick.xmin) * self.xdata_gap for i in ticks]
        else:
            for i in range(len(ticks)):
                ticks[i] = startpos + i * self.xdata_gap

        for tick in ticks:
            pygame.draw.aaline(self.figure.background, GRID_COLOR, (tick, self.y), (tick, self.y + self.height))

    def _draw_horizontal_gridlines(self):
        ticks = self.figure.yaxis_tick.ticks
        startpos = self.y + self.chart_margin
        ticks = [startpos + (self.figure.yaxis_tick.ymax - i) * self.ydata_multiplier for i in ticks]

        for tick in ticks:
            pygame.draw.aaline(self.figure.background, GRID_COLOR, (self.x, tick), (self.x + self.width, tick))

    def _draw_gridlines(self):
        if self.gridlines:
            self._draw_horizontal_gridlines()
            self._draw_vertical_gridlines()



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