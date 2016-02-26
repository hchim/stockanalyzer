import matplotlib.pyplot as plt


def normalize_data(df):
    return df/df.iloc[0]

def plot_multi_symbols(prices, title="Stock Prices", xlabel="Date", ylabel="Price", normalize=False):
    """
    Plot multiple symbols

    Parameters
    ----------
    prices: DataFrame
        prices of the symbols
    title: string
        the title of the figure
    xlabel: string
        the x axis of the figure
    ylabel: string
        the y axis of the figure
    normalize: boolean
    """
    if normalize:
        prices = normalize_data(prices)

    ax = prices.plot(title=title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.show()


def plot_scatter(data, beta, alpha, y_symbol, x_symbol = "SPY"):
    data.plot(kind='scatter', x=x_symbol, y=y_symbol) # draw scatter figure
    plt.plot(data[x_symbol], beta*data[x_symbol] + alpha, '-', color='r')
    plt.show()


def plot_histogram(data, bins=20):
    data.hist(bins=bins)
    plt.show()


def plot_compare_data(x, y1, y2, xlabel="X", y1_label="Y1", y2_label="Y2"):
    fig, ax1 = plt.subplots()
    # two y axis
    ax2 = ax1.twinx()
    ax2.plot(x, y2, color="purple", lw=0.5, ls="--")
    ax2.axhline(0, color="black")
    ax2.set_ylabel(y2_label)

    ax1.plot(x, y1, color="black")
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(y1_label)

    plt.show()
