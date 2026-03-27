export default interface outputData {
  netz_einspeisung_kwh: number;
  netz_bezug_kwh: number;
  ecar: number;
  solar: number;
  household: number;
  heat_pump: number;
  controllable_load: number;

  cost_dynamic: number;
  cost_const: number;
  savings_dynamic: number;

  guenstig_m: number;
  ersparnis: number;

  cost_modul_1: number;
  cost_modul_2: number;
  cost_modul_3: number;
}