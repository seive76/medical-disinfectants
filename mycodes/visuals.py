# Define a function called plot_timeseries
def plot_timeseries(axes, x, y, color, xlabel, ylabel):
    """ 라인시각화 작업
    axes =  plt패기지 'ax'항목 
    x = x축 값 제시
    y = y축 값 제시
    color = 라인선 색깔
    xlabel = x축 이름
    ylabel = y축 이름
    """

  # Plot the inputs x,y in the provided color
  axes.plot(x, y, color=color)

  # Set the x-axis label
  axes.set_xlabel(xlabel) 

  # Set the y-axis label
  axes.set_ylabel(ylabel, color = color) 

  # Set the colors tick params for y-axis
  axes.tick_params('y', colors=color)