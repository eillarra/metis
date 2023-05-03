interface Region {
  id: number;
  name: string;
  country: string;
}

interface Institution {
  id: number;
  name: string;
  type: string;
  region: Region | null;
}
