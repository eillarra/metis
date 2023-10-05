interface Timesheet extends ApiObject {
  date: string;
  start_time_am: string;
  end_time_am: string;
  start_time_pm: string;
  end_time_pm: string;
  duration: string;
  is_approved: boolean;
}
