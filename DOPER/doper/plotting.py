# Distributed Optimal and Predictive Energy Resources (DOPER) Copyright (c) 2019
# The Regents of the University of California, through Lawrence Berkeley
# National Laboratory (subject to receipt of any required approvals
# from the U.S. Dept. of Energy). All rights reserved.

""""Distributed Optimal and Predictive Energy Resources
Plotting module.
"""

# pylint: disable=invalid-name, too-many-locals, too-many-arguments, dangerous-default-value
# pylint: disable=undefined-variable, unused-argument

import numpy as np
import matplotlib.pyplot as plt

def plot_dynamic_nodes(df, parameter, plotFile = None):
    '''
        A standard plotting template to present results.

        Input
        -----
            df (pandas.DataFrame): The resulting dataframe with the optimization result.
            plot (bool): Flag to plot or return the figure. (default=True)
            plot_times (bool): Flag if time separation should be plotted. (default=True)
            tight (bool): Flag to use tight_layout. (default=True)
            
        Returns
        -------
            None if plot == True.
            else:
                fig (matplotlib figure): Figure of the plot.
                axs (numpy.ndarray of matplotlib.axes._subplots.AxesSubplot): Axis of the plot.
    '''

    # number of plot rows is equal to the number of nodes
    n = len(parameter['network']['nodes'])
    fig, axs = plt.subplots(nrows=n,ncols=2, figsize=(24, 3*n), sharex=True, sharey=True)

    # loop through nodes
    for nn, node in enumerate(parameter['network']['nodes']):

        # get node name in order to extract data cols from df
        nodeName = node['node_id']

        # define node-specific col names
        importCol = f'Node grid import [kW] {nodeName}'
        exportCol = f'Node grid export [kW] {nodeName}'
        loadServedCol = f'Node load served [kW] {nodeName}'
        pvGenCol = f'Node pv gen [kW] {nodeName}'
        injPowerCol = f'Node power injected [kW] {nodeName}'
        absPowerCol = f'Node power absorbed [kW] {nodeName}'
        gensetCol = f'Node genset gen [kW] {nodeName}'
        # batChargeCol = f'Node grid import [kW] {nodeName}'
        # batDischargeCol = f'Node grid import [kW] {nodeName}'
        # loadShedCol = f'Node grid import [kW] {nodeName}'

        # create energy provision plot

        # list of provision columns in results df
        provision_cols = [importCol, absPowerCol]
        consumption_cols = [exportCol, loadServedCol, injPowerCol]
        if parameter['system']['pv']:
            provision_cols += [pvGenCol]
        if parameter['system']['genset']:
            provision_cols += [gensetCol]
        # if parameter['system']['battery']:
        #     provision_cols += ['Battery Discharging Power [kW]']
        #     consumption_cols += ['Battery Charging Power [kW]']
        # if parameter['system']['load_control']:
        #     provision_cols += ['Total Shed Load [kW]']

        df[provision_cols].plot.area(ax=axs[nn, 0], \
            title='Energy Provision').legend(loc='upper right')
        df[consumption_cols].plot.area(ax=axs[nn, 1], \
            title='Energy Consumption').legend(loc='upper right')

    if plotFile:
        plt.savefig(plotFile, dpi=300)
    return fig, axs

def plot_pv_only(df, plot=True, plotFile = None, tight=True, plot_reg=None, times=[8,12,18,22]):
    '''
        A standard plotting template to present results.

        Input
        -----
            df (pandas.DataFrame): The resulting dataframe with the optimization result.
            plot (bool): Flag to plot or return the figure. (default=True)
            plot_times (bool): Flag if time separation should be plotted. (default=True)
            tight (bool): Flag to use tight_layout. (default=True)
            
        Returns
        -------
            None if plot == True.
            else:
                fig (matplotlib figure): Figure of the plot.
                axs (numpy.ndarray of matplotlib.axes._subplots.AxesSubplot): Axis of the plot.
    '''
    n = 3
    fig, axs = plt.subplots(n,1, figsize=(12, 3*n), sharex=True, sharey=False,
                           gridspec_kw={'width_ratios':[1]})
    axs = axs.ravel()
    plot_streams(axs[0], df[['Import Power [kW]','Export Power [kW]']], times=times)

    # create energy provision plot
    plot_streams(axs[2], df[['Tariff Energy [$/kWh]']], times=times)
    if plotFile:
        plt.savefig(plotFile)
    if plot:
        if tight:
            plt.tight_layout()
        plt.show()
    return fig, axs

def plot_standard1(df, plot=True, tight=True, plot_reg=None, times=[8,12,18,22]):
    '''
        A standard plotting template to present results.

        Input
        -----
            df (pandas.DataFrame): The resulting dataframe with the optimization result.
            plot (bool): Flag to plot or return the figure. (default=True)
            plot_times (bool): Flag if time separation should be plotted. (default=True)
            tight (bool): Flag to use tight_layout. (default=True)
            
        Returns
        -------
            None if plot == True.
            else:
                fig (matplotlib figure): Figure of the plot.
                axs (numpy.ndarray of matplotlib.axes._subplots.AxesSubplot): Axis of the plot.
    '''
    # Check if include regulation
    if plot_reg is None and df[['Reg Up [kW]','Reg Dn [kW]',
                                'Tariff Reg Up [$/kWh]',
                                'Tariff Reg Dn [$/kWh]']].abs().sum().sum() > 0:
        plot_reg = True
    n = 4 + (2 if plot_reg else 0)
    fig, axs = plt.subplots(n,1, figsize=(12, 3*n), sharex=True, sharey=False,
                            gridspec_kw={'width_ratios':[1]})
    axs = axs.ravel()
    plot_streams(axs[0], df[['Import Power [kW]','Export Power [kW]']], times=times)

    # create energy provision plot
    if 'Battery Power [kW]' in df.columns:
        plot_streams(axs[1], df[['Battery Power [kW]','Load Power [kW]','PV Power [kW]']],
                         times=times)
    else:
        plot_streams(axs[1], df[['Load Power [kW]','PV Power [kW]']],
                         times=times)

    plot_streams(axs[2], df[['Tariff Energy [$/kWh]']], times=times)
    plot_streams(axs[3], df[['Battery SOC [%]']], times=times)
    if plot_reg:
        plot_streams(axs[4], df[['Reg Up [kW]','Reg Dn [kW]']], times=times)
        plot_streams(axs[5], df[['Tariff Reg Up [$/kWh]','Tariff Reg Dn [$/kWh]']], times=times)
    if plot:
        if tight:
            plt.tight_layout()
        plt.show()
    return fig, axs

def plot_dynamic(df, parameter, plot=True,  plotFile = None,
                 tight=True, plot_reg=None, times=[8,12,18,22]):
    '''
        A standard plotting template to present results.

        Input
        -----
            df (pandas.DataFrame): The resulting dataframe with the optimization result.
            plot (bool): Flag to plot or return the figure. (default=True)
            plot_times (bool): Flag if time separation should be plotted. (default=True)
            tight (bool): Flag to use tight_layout. (default=True)
            
        Returns
        -------
            None if plot == True.
            else:
                fig (matplotlib figure): Figure of the plot.
                axs (numpy.ndarray of matplotlib.axes._subplots.AxesSubplot): Axis of the plot.
    '''

    # number of subplots. eventually dynamically determined
    n = 4

    if parameter['system']['battery']:
        # if batteries are enabled, add plot for SOC
        n += 1

    fig, axs = plt.subplots(n,1, figsize=(12, 3*n), sharex=True, sharey=False,
                            gridspec_kw={'width_ratios':[1]})
    axs = axs.ravel()
    # plot_streams(axs[0], df[['Import Power [kW]','Export Power [kW]']], times=times)
    df[['Import Power [kW]','Export Power [kW]']].plot(ax=axs[0], title = 'Power Flow at PCC')

    # create energy provision plot

    # list of provision columns in results df
    provision_cols = ['Import Power [kW]']
    consumption_cols = ['Load Power [kW]', 'Export Power [kW]']
    if parameter['system']['pv']:
        provision_cols += ['PV Power [kW]']
    if parameter['system']['genset']:
        provision_cols += ['Genset Power [kW]']
    if parameter['system']['battery']:
        provision_cols += ['Battery Discharging Power [kW]']
        consumption_cols += ['Battery Charging Power [kW]']
    if parameter['system']['load_control']:
        provision_cols += ['Total Shed Load [kW]']

    df[provision_cols].plot(ax=axs[1], title='Energy Provision').legend(loc='upper right')
    df[consumption_cols].plot(ax=axs[2], title='Energy Consumption').legend(loc='upper right')
    if parameter['system']['battery']:
        df[['Battery Aggregate SOC [-]']].plot(ax=axs[3], title='Battery SOC')
    df[['Tariff Energy [$/kWh]']].plot(ax=axs[n-1], title='Tariff Energy Price')

    if plotFile:
        plt.savefig(plotFile, dpi=300)
    if plot:
        if tight:
            plt.tight_layout()
        plt.show()
    return fig, axs

def my_plot_dynamic(df, parameter, plot=True,  plotFile = None,
                 tight=True, plot_reg=None, times=[8,12,18,22]):
    '''
        A standard plotting template to present results.

        Input
        -----
            df (pandas.DataFrame): The resulting dataframe with the optimization result.
            plot (bool): Flag to plot or return the figure. (default=True)
            plot_times (bool): Flag if time separation should be plotted. (default=True)
            tight (bool): Flag to use tight_layout. (default=True)
            
        Returns
        -------
            None if plot == True.
            else:
                fig (matplotlib figure): Figure of the plot.
                axs (numpy.ndarray of matplotlib.axes._subplots.AxesSubplot): Axis of the plot.
    '''
    custom_legends = {
        'Import Power [kW]': 'Importación [kW]',
        'Load Power [kW]': 'Demanda Pasto [kW]',
        'Battery Charging Power [kW]': 'Carga de baterías [kW]',
        'Battery Discharging Power [kW]': 'Descarga de baterías [kW]',
        'Tariff Energy [$/kWh]': 'Tarifa de energía [USD/kWh]',
        'Battery Aggregate SOC [-]': 'Estado de carga SoC [%]'
    }
    # number of subplots. eventually dynamically determined
    n = 3

    if parameter.get('system', {}).get('battery', False):
        n += 1

    fig, axs = plt.subplots(n, 1, figsize=(12, 3 * n), sharex=True, sharey=False)
    axs = axs.ravel()

    # ----------- Gráfico 1: Importación y carga -----------
    cols_1 = ['Import Power [kW]', 'Load Power [kW]']
    labels_1 = [custom_legends.get(col, col) for col in cols_1] if custom_legends else cols_1
    df[cols_1].plot(ax=axs[0], title='Importación / Demanda en el PCC')
    axs[0].legend(labels_1)

    # ----------- Gráfico 2: Potencia batería -----------
    battery_cols = []
    if parameter['system'].get('battery'):
        battery_cols = ['Battery Discharging Power [kW]', 'Battery Charging Power [kW]']
        labels_bat = [custom_legends.get(col, col) for col in battery_cols] if custom_legends else battery_cols
        df[battery_cols].plot(ax=axs[1], title='Energía de las baterías')
        axs[1].legend(labels_bat, loc='upper right')
    else:
        axs[1].set_visible(False)

    # ----------- Gráfico 3: Tarifa de energía -----------
    col_tariff = 'Tariff Energy [$/kWh]'
    label_tariff = custom_legends.get(col_tariff, col_tariff) if custom_legends else col_tariff
    df[[col_tariff]].plot(ax=axs[2], title='Tarifa de energía')
    axs[2].legend([label_tariff])

    # ----------- Gráfico 4: SoC de batería (si aplica) -----------
    if parameter['system'].get('battery'):
        col_soc = 'Battery Aggregate SOC [-]'
        label_soc = custom_legends.get(col_soc, col_soc) if custom_legends else col_soc
        df[[col_soc]].plot(ax=axs[n - 1], title='Estado de carga (SoC)')
        axs[n - 1].legend([label_soc])

    # Guardar o mostrar
    if plotFile:
        plt.savefig(plotFile, dpi=300)

    if plot:
        if tight:
            plt.tight_layout()
        plt.show()
        return None
    else:
        return fig, axs

def formatExternalData(df):
    '''
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''

    supplyList = ['pvGen', 'genset', 'gridImport', 'powerAbs', 'batDischarge']
    demandList = ['gridExport', 'load',  'powerInj', 'batCharge']

    # set index to col
    # df['ts'] = df.index
    df['ts'] = np.arange(len(df))

    # melt df
    df = df.melt(id_vars=['ts'])

    # create node col
    df[['src', 'node']] = df['variable'].str.split('_', 1, expand=True)

    # drop variable col
    df.drop(['variable'], axis=1, inplace=True)

    # add group based on source
    df['group'] = 'NA'
    df.group[df.src.isin(supplyList)] = 'supply'
    df.group[df.src.isin(demandList)] = 'demand'

    # return reformatted df
    return df
