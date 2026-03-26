export default interface inputData {
    pv: PV,
    ev: EV,
    battery: Battery,
    heat_pump: HeatPump,
    household: Household
}
// PLZ
export interface PV {
    present: boolean,
    power: number,
    direction: "North" | "East" | "South" | "West",
    angle: number
}

export interface Battery {
    present: boolean,
    capacity: number
}

export interface EV {
    present: boolean,
    milage: number,
    has_wall_box: boolean,
}

export interface HeatPump {
    present: boolean,
    yearly_consumption: number
}

export interface Household {
    consumption: number,
    zip_code: String,
}

export const defaultData: inputData = {
    pv: {
        present: false,
        power: 10, 
        direction: "South",
        angle: 35,
    },
    ev: {
        present: false,
        has_wall_box: false, 
        milage: 13000
    },
    battery: {
        present: false,
        capacity: 10
    },
    heat_pump: {
        present: false,
        yearly_consumption: 5000
    },
    household: {
        consumption: 3200,
        zip_code: "01067",
    }
}