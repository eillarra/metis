interface UserTiny extends ApiObject {
  name: string;
  email: string;
}

interface UserLastLogin extends UserTiny {
  last_login: string | null;
}

interface User extends UserLastLogin {
  username: string;
  is_active: boolean;
  date_joined: string;
}
