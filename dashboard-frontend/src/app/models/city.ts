export class City {
  name: string;

  confirmed: number;
  active: number;
  recoveries: number;
  mortalities: number;

  daily: [];
  cumulative: [];

  private latestData;
  private secondLatestData;

  constructor(
    name: string,
    confirmed: number,
    active: number,
    recoveries: number,
    mortalities: number,
    daily: [],
    cumulative: []) {

    this.name = name;
    this.confirmed = confirmed;
    this.active = active;
    this.recoveries = recoveries;
    this.mortalities = mortalities;
    this.daily = daily;
    this.cumulative = cumulative;

    this.latestData = this.cumulative[this.cumulative.length - 1];
    this.secondLatestData = this.cumulative[this.cumulative.length - 2];
  }

  getConfirmedChange(): number {
    return this.latestData['Confirmed'] - this.secondLatestData['Confirmed'];
  }

  getActiveChange(): number {
    return this.latestData['Active'] - this.secondLatestData['Active'];
  }

  getRecoveriesChange(): number {
    return this.latestData['Recoveries'] - this.secondLatestData['Recoveries'];
  }

  getMortalitiesChange(): number {
    return this.latestData['Mortalities'] - this.secondLatestData['Mortalities'];
  }
}
