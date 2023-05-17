interface UserTiny extends ApiObject {
  name: string;
  email: string;
}

interface User extends UserTiny {
  username: string;
  is_active: boolean;
  last_login: string | null;
  date_joined: string;
}
