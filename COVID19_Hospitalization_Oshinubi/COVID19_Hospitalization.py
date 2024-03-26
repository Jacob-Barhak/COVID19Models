"""
COVID-19 Hospitalization Models
CC0 license: see http://creativecommons.org/publicdomain/zero/1.0/

To the extent possible under law, Jacob Barhak has waived all copyright and
related or neighboring rights to COVID-19 Hospitalization Models
This work is published from: United States.

This project implements Hospitalization models as prepared by Kayode Isaac Oshinubi
# Hospitalization models are as follows:

## Hospitalization Probability
There are 3 models of hospitalization probability as a function of age


## Hospitalization Time Since Infection
There are 3 models of hospitalization time in days since infection as a function of age

"""
import pandas as pd
import panel as pn
import holoviews as hv
from bokeh.resources import INLINE
# noinspection PyUnresolvedReferences
import hvplot.pandas

def calc_table(value, delimiters, vector):
    """ calculate value per table"""
    value_index = sum([value > delimiter for delimiter in delimiters]) - 1
    return vector[value_index]


def calc_hospitalization_prob(mixture, age):
    """ calculates the probability of hospitalization per age"""
    ret_val = (mixture[0] * calc_table(age, [0, 20, 80, 120], [0.001, 0.008, 0.019]) +
               mixture[1] * calc_table(age, [0, 30, 70, 120], [0.01, 0.03, 0.05]) +
               mixture[2] * calc_table(age, [0, 20, 40, 60, 120], [0.02, 0.033, 0.045, 0.1])
               ) / (mixture[0] + mixture[1] + mixture[2])
    return ret_val


def calc_hospitalization_day(mixture, age):
    """ calculates the hospitalization time since infection per age"""
    ret_val = (mixture[0] * calc_table(age, [0, 20, 80, 120], [10, 6, 5]) +
               mixture[1] * calc_table(age, [0, 20, 80, 120], [15, 10, 6]) +
               mixture[2] * calc_table(age, [0, 20, 40, 60, 120], [14, 10, 10, 7])
               ) / (mixture[0] + mixture[1] + mixture[2])
    return ret_val


def create_plots():
    """plot the function for each age group and time"""
    hv.extension('bokeh')
    pn.extension(safe_embed=True)

    height = 200
    width = 800

    prob_models = [
        'Model 1: Low probability',
        'Model 2: Moderate Probability',
        'Model 3: High Probability',
    ]

    time_models = [
        'Model 1: Early Hospitalization',
        'Model 2: Late Hospitalization',
        'Model 3: Mixed Hospitalization',
    ]

    ages = list(range(5, 100, 5))
    x_label = 'Age in Years'

    for (y_label, func, model_list) in \
            [('Hospitalization Prob', calc_hospitalization_prob, prob_models),
             ('Hospitalization Time', calc_hospitalization_day, time_models)]:
        plot_data = []
        for model_enum in range(len(model_list)):
            prob_mixture = [model_enum == running_enum for running_enum in range(len(model_list))]
            plot_data_part = [{'model': model_list[model_enum],
                               x_label: age,
                               y_label: func(prob_mixture, age)
                               }
                              for age in ages
                              ]
            plot_data.extend(plot_data_part)
        y_data = [entry[y_label] for entry in plot_data]
        y_lim = (0, max(y_data))

        dict_df = pd.DataFrame(plot_data)
        plot = dict_df.hvplot.bar(x_label, y_label, groupby='model',
                                  height=height, width=width).opts(ylim=y_lim,
                                                                   toolbar=None,
                                                                   default_tools=[])
        panel_object = pn.panel(plot)
        panel_object.save('COVID19_' + y_label.replace(' ', '_'), embed=True, resources=INLINE)


if __name__ == '__main__':
    create_plots()
