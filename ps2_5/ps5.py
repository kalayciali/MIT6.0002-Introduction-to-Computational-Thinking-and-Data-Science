# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Ali Kalaycı  @phymat


import pylab
import re

# regular expressions library
# someone who is curious may find info at this site:
# https://docs.python.org/3/howto/regex.html#

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    models= []
    for deg in degs:
        model= pylab.polyfit(x, y, deg)
        models.append(model)
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    num= ((y- estimated)**2).sum()
    denom= ((y- y.mean())**2).sum()
    R2= 1- num/denom
    return R2

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        estimated= pylab.polyval(model, x)
        R2= r_squared(y, estimated)
        if len(model) == 2:
            SE_slope= se_over_slope(x, y, estimated, model)
            pylab.figure()
            pylab.plot(x, y, 'bo', label= 'data')
            pylab.plot(x, estimated, 'r', label= 'model')
            pylab.title('Degree= '+ str(len(model)-1) + ', R2= '+ str(round(R2, 4))+ 
                        '\n SE_slope= '+ str(round(SE_slope, 4)))
            pylab.legend(loc= 'best')
            pylab.xlabel('years')
            pylab.ylabel('temp')
            pylab.savefig('eval_on_train'+ str(models.index(model)+ 1)+ '.png')
            continue
        pylab.figure()
        pylab.plot(x, y, 'bo', label= 'data')
        pylab.plot(x, estimated, 'r', label= 'model')
        pylab.title('Degree= '+ str(len(model)-1) + ', R2= '+ str(round(R2, 4)))
        pylab.legend(loc= 'best')
        pylab.xlabel('years')
        pylab.ylabel('temp')
        pylab.savefig('eval_on_train'+ str(models.index(model))+ '.png')
        
        
        

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    # TODO
    temps_year= []
    for year in years:
        temps_city= []
        for city in multi_cities:
            temps= climate.get_yearly_temp(city, year)
            temps_city.append(temps.sum()/ len(temps))
        temps_year.append(sum(temps_city)/ len(temps_city))
    return pylab.array(temps_year)

def moving_average(y, window):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    mov_avg= []
    i= 1
    while i != len(y)+ 1 :
        if i < window:
            mov_avg.append( y[:i].sum() / len(y[:i]))
            i +=1
            continue
        mov_avg.append( y[(i - window):i].sum() / window)
        i +=1
    return pylab.array(mov_avg)  

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # TODO
    num= ((y- estimated)**2).sum()
    rmse= pylab.sqrt(num/len(y))
    return rmse

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    temps_year= []
    for year in years:
        temps_city= []
        for city in multi_cities:
            temps= climate.get_yearly_temp(city, year)
            temps_city.append(temps.sum()/ len(temps))
        temps_year.append(pylab.std(temps_city))
    return pylab.array(temps_year)


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    # TODO
    for model in models:
        estimated= pylab.polyval(model, x)
        RMSE= rmse(y, estimated)
        pylab.figure()
        pylab.plot(x, y, 'bo', label= 'data')
        pylab.plot(x, estimated, 'r', label= 'model')
        pylab.title('Degree= '+ str(len(model)-1) + ', RMSE= '+ str(round(RMSE, 4)))
        pylab.legend(loc= 'best')
        pylab.xlabel('years')
        pylab.ylabel('temp')
        pylab.savefig('eval_on_train'+ str(models.index(model))+ '.png')
        

if __name__ == '__main__':

    pass 
    data= Climate('data.csv')
    # Part A.4
    # TODO: replace this line with your code
#    temps= []
#    years= []
#    for year in TRAINING_INTERVAL:
#        temps.append(data.get_daily_temp('NEW YORK', 1, 10, year))
#        years.append(year)
#    x= pylab.array(years)
#    y= pylab.array(temps)
#    model= generate_models(x, y, (1, ))
#    evaluate_models_on_training(x, y, model)
    
    # Part B
    # TODO: replace this line with your code
#    avg_temps= []
#    years= []
#    for year in TRAINING_INTERVAL:
#        temps= data.get_yearly_temp('NEW YORK', year)
#        avg_temps.append(temps.sum()/ len(temps))
#        years.append(year)
#    x= pylab.array(years)
#    y= pylab.array(avg_temps)
#    model= generate_models(x, y, (1, ))
#    evaluate_models_on_training(x, y, model)

    # Part C
    # TODO: replace this line with your code
#    years= pylab.array([i for i in TRAINING_INTERVAL])
#    nation_avg = gen_cities_avg(data, CITIES, years)
#    model= generate_models(years, nation_avg, (1, ))
#    evaluate_models_on_training(years, nation_avg, model)
    
    # Part D.2
    # TODO: replace this line with your code
#    years= pylab.array([i for i in TRAINING_INTERVAL])
#    nation_avg = gen_cities_avg(data, CITIES, years)
#    mov_avg= moving_average(nation_avg, 5)
#    model= generate_models(years, mov_avg, (1, ))
#    evaluate_models_on_training(years, mov_avg, model)
    # testing our model
    years= pylab.array([i for i in TRAINING_INTERVAL])
    nation_avg = gen_cities_avg(data, CITIES, years)
    mov_avg= moving_average(nation_avg, 5)
    models= generate_models(years, mov_avg, (1, 2, 20))
#    evaluate_models_on_training(years, mov_avg, models)
    
    
    test_years= [i for i in TESTING_INTERVAL]
    nation_avg_test = gen_cities_avg(data, CITIES, test_years)
    mov_avg_test= moving_average(nation_avg_test, 5)
#    evaluate_models_on_testing(test_years, mov_avg_test, models)
    
    # Part E
    # TODO: replace this line with your code
    years= pylab.array([i for i in TRAINING_INTERVAL])
    std_devs= gen_std_devs(data, CITIES, years)
    mov_std= moving_average(std_devs, 5)
    model= generate_models(years, mov_std, (1, ))
#    evaluate_models_on_training(years, mov_std, model)
    
