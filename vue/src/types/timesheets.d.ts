interface TimesheetData {
  comments?: string;
  weekly_reflection?: string;
  weekly_action_points?: string;
}

interface Timesheet extends ApiObject {
  date: string;
  start_time_am: string;
  end_time_am: string;
  start_time_pm: string;
  end_time_pm: string;
  duration: string;
  is_approved: boolean;
  data: TimesheetData;
}
