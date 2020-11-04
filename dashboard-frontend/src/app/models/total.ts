export class Total {
  confirmed: number;
  active: number;
  recoveries: number;
  mortalities: number;
  critical: number;
  tested: number;

  daily: [];
  cumulative: [];

  private latestData;
  private secondLatestData;

  constructor(
    confirmed: number,
    active: number,
    recoveries: number,
    mortalities: number,
    critical: number,
    tested: number,
    daily: [],
    cumulative: []) {

    this.confirmed = confirmed;
    this.active = active;
    this.recoveries = recoveries;
    this.mortalities = mortalities;
    this.tested = tested;
    this.critical = critical;

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
