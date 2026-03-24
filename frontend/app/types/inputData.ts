export default interface inputData {
    pv?: PV,
    ev?: EV,
    battery?: Battery,
    heat_pump?: HeatPump,
    household: Household
}

export interface PV {
    power: number,
    direction: "North" | "East" | "South" | "West",
    angle: number
}

export interface Battery {
    capacity: number
}

export interface EV {
    milage: number,
    charging_time: number,
    charging_power: number,
}

export interface HeatPump {
    yearly_consumption: number
}

export interface Household {
    consumption?: number,
    people?: number,
}

// consumption: 4500,
// currentPrice: 32.5,
// baseFee: 15,
// hasEV: false,
// hasHeatPump: false,
// hasBattery: false,
// shiftablePercentage: 20