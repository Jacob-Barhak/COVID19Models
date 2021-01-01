# COVID-19 mortality model by Filippo Castiglione et. al. 
# This work is available under MIT license
# Copyright 2020 Filippo Castiglione
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

# This program calculates the probability of Mortality according to the paper:
# Filippo Castiglione, Debashrito Deb, Anurag P. Srivastava, Pietro Liò, Arcangelo Liso
# bioRxiv 2020.12.20.423670; doi: https://doi.org/10.1101/2020.12.20.423670
# supplemented with communications in the comodbidities and integration 
# subgroups mailing lists of the multi scale modeling and viral pandemic 
# working group - those are archived in those links:
# https://lists.simtk.org/pipermail/vp-integration-subgroup/2020-December/thread.html
# https://lists.simtk.org/pipermail/vpcomorbidities-subgroup/2020-December/thread.html


# Filippo Castiglione the first Author of the paper agreed Jacob Barhak can release 
# this code under a license of choice seen on: 
# https://lists.simtk.org/pipermail/vpcomorbidities-subgroup/2020-December/000007.html
# Initial permission to replicate the code was released in:
# https://lists.simtk.org/pipermail/vpcomorbidities-subgroup/2020-December/000002.html


# Here is the differentiation of the original function using sympy
# from sympy import symbols, exp, diff
# a, b ,c, x = symbols('a b c x')
# f = 100 - ( a / (1+exp(-b*(x-c))))
# p = 1-f/100
# diff(p,x)
#
# -a*b*exp(-b*(-c + x))/(1 + exp(-b*(-c + x)))**2
# note that x here stands for time since infection in 8 hour periods

from math import exp


def mortality_prob(age, time):
    """ Calculate probability of COVID-19 mortality as a function of age 
        and time from infection in days - this is the density function
    """
    # We construct a table of parameters per age decade: as extracted from
    # the instructions in the emails. Each line in the matrix corresponds to
    # a decade of age and include the following coefficients:
    # [ multiplier , a, b, c]
    # where multiplier stands for the coefficient in figure 3A per age group
    mortality_coefficients = [ 
       [  0.39, 96.56299632152,   0.185777403544838, 49.8164210315686 ], # [0-10)
       [  0.79, 96.56299632152,   0.185777403544838, 49.8164210315686 ], # [10-20)
       [  0.79, 96.56299632152,   0.185777403544838, 49.8164210315686 ], # [20-30)
       [  0.79, 96.56299632152,   0.185777403544838, 49.8164210315686 ], # [30-40)
       [  1.25, 95.351153808322,  0.173066025988826, 51.92498287875   ], # [40-50)
       [  2.38, 94.2976479245251, 0.165018635066338, 54.1494851021362 ], # [50-60)
       [  4.80, 91.3990353489634, 0.158299883031816, 55.5935133562513 ], # [60-70)
       [  7.35, 88.9048923236574, 0.152924609509616, 57.7447222979953 ], # [70-80)
       [ 12.25, 85.6674967019556, 0.14040123117131 , 61.383806850923  ], # [80+)
    ]        
    # calculate the age index to the coefficients 
    # all ages after 80 are considered as 80+
    age_index = int(min(age, 80) // 10)
    [multiplier, a, b, c] = mortality_coefficients[age_index]
    # the x in the equation is time in 8 hour periods = 1/3 day.
    # so the conversion to x is:
    x = time * 3.0
    # since this is a density function and we divided  time by 3 we need to 
    # compensate and multiply the intensity by 3 - this is beyond the 
    # previous instructions that multiply by a multiplier and divide by 100
    prob = 3 * multiplier / 100 * (a*b*exp(-b*(-c + x))/(100*(1 + exp(-b*(-c + x)))**2))
    # for simplicity note that this result assuming rectangular integration over 1 day
    # should reflect the probability of mortality in a specific day.
    return prob


def create_plots():
    """plot the function for each age group and time"""
    # graphics imports are needed only for the plot function
    # this way the file can be imported only for function 
    # calculation with only basic python
    import panel as pn
    import holoviews as hv
    from bokeh.resources import INLINE
    hv.extension('bokeh')
    pn.extension(safe_embed=True)
    ages = [i for i in range(0, 100, 10)]
    times = [i for i in range(50)]
    plot_dict = {}
    x_label = 'Time since infection in days'
    y_label = 'Mortality probability'
    for age in ages:
        probabilities = [mortality_prob(age, time) for time in times]
        data = {x_label: times, y_label: probabilities}        
        single_plot = hv.Points(data, kdims=[x_label, y_label])
        plot_dict[age] = single_plot     
    hmap = hv.HoloMap(plot_dict, kdims=['age']).opts(height=600, width=800, tools=['hover'], 
                     title = 'Daily Probability of COVID-19 Mortality by Age and Time Since Infection')
    panel_object = pn.pane.HoloViews(hmap)
    panel_object.save('COVID19_Mortality_Castiglione', embed=True, resources=INLINE)     


if __name__ == '__main__':
    create_plots()
