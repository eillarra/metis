interface EmailAddressObject {
  email: EmailAddress;
  verified: boolean;
  primary: boolean;
}

interface UserTiny extends ApiObject {
  name: string;
  email: EmailAddress;
}

interface UserLastLogin extends UserTiny {
  last_login: string | null;
}

interface User extends UserLastLogin {
  username: string;
  is_active: boolean;
  date_joined: string;
}

interface AuthenticatedUser extends User {
  rel_addresses: ApiEndpoint;
}
