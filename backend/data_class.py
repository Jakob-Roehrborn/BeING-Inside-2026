from dataclasses import dataclass
from pydantic import BaseModel

# ---- input Data ----

@dataclass
class Coordinates:
    latitude: float
    longitude: float

class GeneralInfo(BaseModel):
    postal_code: str
    coordinates: Coordinates | None = None
    total_consumption: int
    eprice: float
    smart: bool

class SolarSystem(BaseModel):
    exist: bool
    azimuth: int
    tilt: int
    capacity_kwp: float

class HeatPump(BaseModel):
    exist: bool
    performance_kWh_year: int

class ECar(BaseModel):
    exist: bool
    ziel_jahreskilometer: int
    verbrauch_kwh_pro_100km: float
    wallbox: bool
    start_ladezeit : float
    akku_grosse : int
    anteil_zu_Hause : float

class Memory(BaseModel):
    exist: bool
    capacity_kWh: float


class input_data(BaseModel):
    general_info: GeneralInfo
    solar_system: SolarSystem
    heat_pump: HeatPump
    ecar: ECar
    memory: Memory

def input_to_class(data: dict) -> input_data:
    gen_dict = data["general_info"].copy()
    gen_dict["coordinates"] = Coordinates(**gen_dict["coordinates"])
    return input_data(
        general_info=GeneralInfo(**gen_dict),
        solar_system =SolarSystem(**data["solar_system"]),
        heat_pump = HeatPump(**data["heat_pump"]),
        ecar = ECar(**data["ecar"]),
        memory = Memory(**data["memory"]),
    )

# ----- output Data -----

class output_data(BaseModel):
    netz_einspeisung_kwh: float
    netz_bezug_kwh: float
    ecar: float
    solar: float
    household: float
    heat_pump: float
    controllable_load: float
    eigenverbrauch_p: float

    cost_dynamic: float
    cost_const: float
    savings_dynamic: float

    cost_modul_1: float
    cost_modul_2: float
    cost_modul_3: float