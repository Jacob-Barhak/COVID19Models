# COVID-19 Infectiousness Models from Multiple Sources 
# CC0 license: see http://creativecommons.org/publicdomain/zero/1.0/
#
# To the extent possible under law, Jacob Barhak has waived all copyright and 
# related or neighboring rights to COVID-19 Infectiousness Models from Multiple Sources
# This work is published from: United States.
# 
# This project implements infectiousness profiles per day since infection as extracted from multiple sources:
# Infectiousness models are as follows:
### Model 1
# Based on Table 1 in:
# * Ruiyun Li, Sen Pei, Bin Chen, Yimeng Song, Tao Zhang, Wan Yang, Jeffrey Shaman. 
#   Substantial undocumented infection facilitates the rapid dissemination of novel coronavirus (SARS-CoV2), 
#   Science  01 May 2020: Vol. 368, Issue 6490, pp. 489-493. https://doi.org/10.1126/science.abb3221
#  (https://science.sciencemag.org/content/sci/early/2020/03/13/science.abb3221.full.pdf)
# The following numbers were extracted:
# Min 3.69   Max 3.69 + 3.48 = 7.17  
# It was assumed that max infectiousness occurs from start to end except from start and end day in which infectiousness is relative to the portion of the day within the infectiousness period. 
#
### Model 2
# Based on hand digitized figure 3G in:
# * Ruian Ke, Carolin Zitzmann, Ruy M. Ribeiro, Alan S. Perelson. Kinetics of SARS-CoV-2 infection in the human 
#   upper and lower respiratory tracts and their relationship with infectiousness.
#   medRxiv 2020.09.25.20201772; [DOI: 10.1101/2020.09.25.20201772](https://doi.org/10.1101/2020.09.25.20201772)
# The numbers were digitized manually and processed by scaling the max y to 1 and averaging over 2 points and 
# rounding both x and y  to the closest 1 digits and remove the fractions
# Any numbers after day 15 were estimated by eye 
#
### Model 3
# Based on hand digitized figure 3C in:
# * Ruian Ke, Carolin Zitzmann, Ruy M. Ribeiro, Alan S. Perelson. Kinetics of SARS-CoV-2 infection in the human 
#   upper and lower respiratory tracts and their relationship with infectiousness.
#   medRxiv 2020.09.25.20201772; https://doi.org/10.1101/2020.09.25.20201772
# The numbers were digitized manually and processed by scaling the max y to 1 and averaging over 2 points and 
# rounding both x and y  to the closest 1 digits and remove the fractions
#
### Model 4
# Based on hand digitized Figure 2a - blue curve from:
# * W.S. Hart, P.K. Maini, R.N. Thompson , High infectiousness immediately before COVID-19 symptom onset highlights 
#   the importance of contact tracing. medRxiv 2020.11.20.20235754; https://doi.org/10.1101/2020.11.20.20235754
# The numbers were digitized manually and processed by scaling the max y to 1 and averaging over 2 points and 
# rounding both x and y  to the closest 1 digits and remove the fractions
### Model 5
# Based on equation 7 from:
# * Lucas Bottcher, Mingtao Xia, Tom Chou. Why case fatality ratios can be misleading: individual- and population-based
#   mortality estimates and factors influencing them. Physical Biology, Volume 17, Number 6. https://doi.org/10.1088/1478-3975/ab9e59
# The numbers were generated using a=8,  b=1.25 , x= np.array(range(19)), b*gamma.pdf(b*x, a) / max(b*gamma.pdf(b*x, a))
# additional information and confirmation available in this online discussion: 
# https://lists.simtk.org/pipermail/vp-integration-subgroup/2021-March/000044.html


def infectiosness_per_day(model_number, days_since_infection):
    """ Calculates the infectiousness per model for day since infection """
    infectiousness_per_day = [  
    #   The commented first line is day and is not used
    #   [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        [0,  0,  0,.31,  1,  1,  1,  1,.17,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,0.3,0.9,  1,  1,  1,  1,  1,  1,  1,  1,  1,0.9,0.9,0.8,0.6,0.4,0.2,  0],
        [0,0.1,0.8,  1,  1,0.9,0.7,0.2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0,0.1,0.4,0.8,  1,  1,0.8,0.6,0.5,0.3,0.2,0.2,0.1,0.1,  0,  0,  0,  0,  0],
        [0.00000000e+00, 1.85046877e-03, 6.78615268e-02, 3.32195953e-01,
         7.13012907e-01, 9.74090662e-01, 1.00000000e+00, 8.42867727e-01,
         6.14943126e-01, 4.01822736e-01, 2.40695980e-01, 1.34384609e-01,
         7.07947994e-02, 3.55195943e-02, 1.70959279e-02, 7.93902445e-03,
         3.57355197e-03, 1.56507290e-03, 6.69008375e-04]
    ]
    relative_infectiousness = infectiousness_per_day[model_number][days_since_infection]
    return relative_infectiousness


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
    models = [
        'Model 1: Table 1 Li et. al. DOI: 10.1126/science.abb3221',
        'Model 2: Figure 3G Ke et. al. DOI: 10.1101/2020.09.25.20201772',
        'Model 3: Figure 3C Ke et. al. DOI: 10.1101/2020.09.25.20201772',
        'Model 4: Figure 2a blue Hart et. al. 10.1101/2020.11.20.20235754',
        'Model 5: Eq 7 Bottcher et. al. 10.1088/1478-3975/ab9e59'
    ]
    times = [i for i in range(19)]
    plot_dict = {}
    x_label = 'Time since infection in days'
    y_label = 'Relative Infectiousness'
    for (model_enum, model) in enumerate(models):
        infectiousness = [infectiosness_per_day(model_enum, time) for time in times]
        data = {x_label: times, y_label: infectiousness}        
        single_plot = hv.Bars(data, kdims=[x_label], vdims=[y_label]).opts(title = 'Relative Infectiousness of COVID-19 Per Day Since Infection', color = 'blue', tools=['hover'])           
        plot_dict[model] = single_plot
    hmap = hv.HoloMap(plot_dict, kdims=['model']).opts(height=600, width=800, 
                     title = 'Relative Infectiousness of COVID-19 Per Day Since Infection')
    panel_object = pn.pane.HoloViews(hmap)
    panel_object.save('COVID19_Infectiousness_Multi', embed=True, resources=INLINE)     


if __name__ == '__main__':
    create_plots()
