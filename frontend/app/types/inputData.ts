export default interface inputData {
    solar_system: SolarSystem,
    ecar: ECar,
    memory: Memory,
    heat_pump: HeatPump,
    general_info: GeneralInfo
}

export interface SolarSystem {
    exist: boolean,
    capacity_kwp: number,
    azimuth: number,
    tilt: number,
    area_sqm: number,
}

export interface Memory {
    exist: boolean,
    capacity_kWh: number
}

export interface ECar {
    exist: boolean,
    ziel_jahreskilometer: number,
    verbrauch_kwh_pro_100km: number,
    wallbox: boolean,
    start_ladezeit: number,
    akku_grosse: number,
    anteil_zu_Hause: number,
}

export interface HeatPump {
    exist: boolean,
    performance_kWh_year: number
}

export interface GeneralInfo {
    total_consumption: number,
    postal_code: String,
    eprice: number,
    smart: boolean,
}

export const defaultData: inputData = {
    solar_system: {
        exist: false,
        capacity_kwp: 10, 
        azimuth: 180,
        tilt: 35,
        area_sqm: 30,
    },
    ecar: {
        exist: false,
        ziel_jahreskilometer: 13000,
        verbrauch_kwh_pro_100km: 14,
        akku_grosse: 64,
        start_ladezeit: 12,
        anteil_zu_Hause: 0.75,
        wallbox: false
    },
    memory: {
        exist: false,
        capacity_kWh: 10
    },
    heat_pump: {
        exist: false,
        performance_kWh_year: 5000
    },
    general_info: {
        total_consumption: 3200,
        postal_code: "01067",
        eprice: 0.37,
        smart: false
    }
}