from drawing import Drawing
from determine_figure import determine_figure

figure_sequence, dimensions = determine_figure("square 10x10 centered")
Drawing(figure_sequence, dimensions).run()