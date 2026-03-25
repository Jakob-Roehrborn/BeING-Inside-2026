from dataclasses import dataclass

@dataclass
class Coordinates:
    latitude: float
    longitude: float

@dataclass
class GeneralInfo:
    postal_code: str
    city: str
    coordinates: Coordinates
    number_of_person: int
    total_consumption: int

@dataclass
class SolarSystem:
    exist: bool
    azimuth: int
    tilt: int
    capacity_kwp: float
    area_sqm: float

@dataclass
class HeatPump:
    exist: bool
    performance_kWh_year: int

@dataclass
class ECar:
    exist: bool
    ziel_jahreskilometer: int
    verbrauch_kwh_pro_100km: float
    max_leistung_kw: float
    wallbox: bool

@dataclass
class Memory:
    exist: bool
    capacity_kWh: float

@dataclass
class Metadata:
    last_updated: str

@dataclass
class input_data:
    general_info: GeneralInfo
    solar_system: SolarSystem
    heat_pump: HeatPump
    ecar: ECar
    memory: Memory
    metadata: Metadata

def input_to_class(data: dict) -> input_data:
    gen_dict = data["general_info"].copy()
    gen_dict["coordinates"] = Coordinates(**gen_dict["coordinates"])
    return input_data(
        general_info=GeneralInfo(**gen_dict),
        solar_system =SolarSystem(**data["solar_system"]),
        heat_pump = HeatPump(**data["heat_pump"]),
        ecar = ECar(**data["ecar"]),
        memory = Memory(**data["memory"]),
        metadata = Metadata(**data["metadata"])
    )