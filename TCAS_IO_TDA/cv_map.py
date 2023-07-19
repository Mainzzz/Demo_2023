variable_map = {
    'CM': {
        'Mode S Address': 'cfgModeSAddress',
        'Tail Number': 'cfgAircraftIdentification'
    },
    'Discrete': {
        'Air Ground': 'cmioXAirGndDsc',
        'Standby': 'cmioXStandbyOnDsc',
        'ADC Select Source': {},
    },
    'Control Pane': {
        'Label 013': 'RawTCASCtrl1',                #TCAS control
        'Label 015': 'RawTCASAL1',                  #TCAS alt limit control
        'Label 016': 'RawTCASMSCtrl1',              #TCAS/Mode S control
        'Label 031': 'cmioModeSCtrl4096IdentCode',  #Mode S control
        'cmioModesCtrlSPI': None,
        'cmioModeSCtrlAltReporting': None
    },
    'From ADC': {
        'Label 203': 'cmioXADCSelectedUncorrectedAlt'
    },
    'From IRS & FMS': {},
    'From GPS': {
        'Label 110': 'cmioSelectedGLat',
        'Label 111': 'cmioSelectedGLng',
        'Label 120': 'cmioSelectedGLatFin',
        'Label 121': 'cmioSelectedGLngFin',
        'Label 130': 'cmioSelectedRAIMNISF1',
        'cmioSelectedGHIL': None,
        'Label 165': 'cmioSelectedGVertVel',
        'Label 166': 'cmioSelectedGNSVel',
        'Label 174': 'cmioSelectedGPSEWVel',
        'Label 247': 'cmioSelectedGHVFOM',
        'Label 370': 'cmioSelectedGHAEAlt'
    }
}

XPDR_TCAS_IO_CV_Map ={
    'Mode S Address': 'cfgModeSAddress',
    'Tail Number': 'cfgAircraftIdentification',
    'Air Ground': 'cmioXAirGndDsc',
    'Standby': 'cmioXStandbyOnDsc',
    'ADC Select Source': {},
    'Label 013': 'RawTCASCtrl1',                #TCAS control
    'Label 015': 'RawTCASAL1',                  #TCAS alt limit control
    'Label 016': 'RawTCASMSCtrl1',              #TCAS/Mode S control
    'Label 031': 'cmioModeSCtrl4096IdentCode',  #Mode S control
    # 'cmioModesCtrlSPI': None,
    # 'cmioModeSCtrlAltReporting': None,
    'Label 203': 'cmioXADCSelectedUncorrectedAlt',
    'Label 110': 'cmioSelectedGLat',
    'Label 111': 'cmioSelectedGLng',
    'Label 120': 'cmioSelectedGLatFin',
    'Label 121': 'cmioSelectedGLngFin',
    'Label 130': 'cmioSelectedRAIMNISF1',
    'cmioSelectedGHIL': None,
    'Label 165': 'cmioSelectedGVertVel',
    'Label 166': 'cmioSelectedGNSVel',
    'Label 174': 'cmioSelectedGPSEWVel',
    'Label 247': 'cmioSelectedGHVFOM',
    'Label 370': 'cmioSelectedGHAEAlt',
    'Label 350 bit 16': 'Label_350_16'
}
