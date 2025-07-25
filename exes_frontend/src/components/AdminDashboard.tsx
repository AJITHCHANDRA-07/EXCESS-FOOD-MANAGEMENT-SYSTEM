import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  PieChart, 
  RefreshCw, 
  AlertTriangle, 
  CheckCircle, 
  MapPin, 
  Users, 
  Package 
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Button } from './ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from './ui/table';
import { Badge } from './ui/badge';

// Types
interface Machine {
  id: string;
  name: string;
  address: string;
  status: 'operational' | 'maintenance' | 'offline';
  availableSpace: number;
  availableFood: number;
  expiredFood: number;
  lastUpdated: string;
}

interface Volunteer {
  id: string;
  name: string;
  email: string;
  status: 'active' | 'inactive';
  lastActivity: string;
  assignedMachines: string[];
}

interface DashboardStats {
  totalMachines: number;
  operationalMachines: number;
  totalDonations: number;
  totalCollections: number;
  totalVolunteers: number;
  activeVolunteers: number;
  totalFoodItems: number;
  expiredFoodItems: number;
}

const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalMachines: 0,
    operationalMachines: 0,
    totalDonations: 0,
    totalCollections: 0,
    totalVolunteers: 0,
    activeVolunteers: 0,
    totalFoodItems: 0,
    expiredFoodItems: 0
  });
  
  const [machines, setMachines] = useState<Machine[]>([]);
  const [volunteers, setVolunteers] = useState<Volunteer[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Fetch dashboard data
  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data
        const mockStats: DashboardStats = {
          totalMachines: 12,
          operationalMachines: 10,
          totalDonations: 245,
          totalCollections: 198,
          totalVolunteers: 15,
          activeVolunteers: 12,
          totalFoodItems: 47,
          expiredFoodItems: 8
        };
        
        const mockMachines: Machine[] = [
          {
            id: 'm1',
            name: 'Downtown Machine',
            address: '123 Main St, Downtown',
            status: 'operational',
            availableSpace: 75,
            availableFood: 12,
            expiredFood: 0,
            lastUpdated: '2025-05-16T08:30:00Z'
          },
          {
            id: 'm2',
            name: 'Westside Machine',
            address: '456 Ocean Ave, Westside',
            status: 'operational',
            availableSpace: 30,
            availableFood: 5,
            expiredFood: 2,
            lastUpdated: '2025-05-16T09:15:00Z'
          },
          {
            id: 'm3',
            name: 'Eastside Machine',
            address: '789 Valley Blvd, Eastside',
            status: 'operational',
            availableSpace: 90,
            availableFood: 0,
            expiredFood: 0,
            lastUpdated: '2025-05-16T07:45:00Z'
          },
          {
            id: 'm4',
            name: 'Northside Machine',
            address: '101 Hill St, Northside',
            status: 'operational',
            availableSpace: 10,
            availableFood: 20,
            expiredFood: 3,
            lastUpdated: '2025-05-16T10:00:00Z'
          },
          {
            id: 'm5',
            name: 'Southside Machine',
            address: '202 Harbor Blvd, Southside',
            status: 'maintenance',
            availableSpace: 50,
            availableFood: 8,
            expiredFood: 3,
            lastUpdated: '2025-05-16T06:30:00Z'
          },
          {
            id: 'm6',
            name: 'Central Park Machine',
            address: '303 Park Ave, Central',
            status: 'offline',
            availableSpace: 0,
            availableFood: 0,
            expiredFood: 0,
            lastUpdated: '2025-05-15T18:45:00Z'
          }
        ];
        
        const mockVolunteers: Volunteer[] = [
          {
            id: 'v1',
            name: 'John Smith',
            email: 'john.smith@example.com',
            status: 'active',
            lastActivity: '2025-05-16T09:30:00Z',
            assignedMachines: ['m1', 'm2']
          },
          {
            id: 'v2',
            name: 'Jane Doe',
            email: 'jane.doe@example.com',
            status: 'active',
            lastActivity: '2025-05-16T08:15:00Z',
            assignedMachines: ['m3', 'm4']
          },
          {
            id: 'v3',
            name: 'Bob Johnson',
            email: 'bob.johnson@example.com',
            status: 'inactive',
            lastActivity: '2025-05-10T14:20:00Z',
            assignedMachines: []
          },
          {
            id: 'v4',
            name: 'Alice Williams',
            email: 'alice.williams@example.com',
            status: 'active',
            lastActivity: '2025-05-15T16:45:00Z',
            assignedMachines: ['m5']
          }
        ];
        
        setStats(mockStats);
        setMachines(mockMachines);
        setVolunteers(mockVolunteers);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleRefresh = () => {
    // Reload dashboard data
    setLoading(true);
    setTimeout(() => setLoading(false), 1000);
  };

  const getStatusBadge = (status: 'operational' | 'maintenance' | 'offline') => {
    switch (status) {
      case 'operational':
        return <Badge className="bg-green-500">Operational</Badge>;
      case 'maintenance':
        return <Badge className="bg-yellow-500">Maintenance</Badge>;
      case 'offline':
        return <Badge className="bg-red-500">Offline</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-green-700">Admin Dashboard</h1>
        <Button onClick={handleRefresh} disabled={loading}>
          <RefreshCw className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Machines</CardTitle>
            <Package className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.operationalMachines}/{stats.totalMachines}</div>
            <p className="text-xs text-gray-500">Operational machines</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Food Items</CardTitle>
            <BarChart className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalFoodItems}</div>
            <p className="text-xs text-gray-500">Available in system</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Volunteers</CardTitle>
            <Users className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.activeVolunteers}/{stats.totalVolunteers}</div>
            <p className="text-xs text-gray-500">Active volunteers</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Transactions</CardTitle>
            <PieChart className="h-4 w-4 text-gray-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalDonations + stats.totalCollections}</div>
            <p className="text-xs text-gray-500">{stats.totalDonations} donations, {stats.totalCollections} collections</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs defaultValue="machines" className="mb-8">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="machines">Machines</TabsTrigger>
          <TabsTrigger value="volunteers">Volunteers</TabsTrigger>
        </TabsList>
        
        {/* Machines Tab */}
        <TabsContent value="machines">
          <Card>
            <CardHeader>
              <CardTitle>Machine Status</CardTitle>
              <CardDescription>
                Overview of all machines in the system. {stats.expiredFoodItems > 0 && (
                  <span className="text-yellow-600 font-medium">
                    {stats.expiredFoodItems} machines have expired food that needs attention.
                  </span>
                )}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-700 mx-auto mb-4"></div>
                  <p>Loading machine data...</p>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Location</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Food Items</TableHead>
                      <TableHead>Space</TableHead>
                      <TableHead>Last Updated</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {machines.map(machine => (
                      <TableRow key={machine.id}>
                        <TableCell className="font-medium">{machine.name}</TableCell>
                        <TableCell>
                          <div className="flex items-center">
                            <MapPin className="h-4 w-4 text-gray-500 mr-1" />
                            <span className="text-sm">{machine.address}</span>
                          </div>
                        </TableCell>
                        <TableCell>{getStatusBadge(machine.status)}</TableCell>
                        <TableCell>
                          <div className="flex items-center">
                            <span className="mr-2">{machine.availableFood}</span>
                            {machine.expiredFood > 0 && (
                              <Badge variant="outline" className="bg-yellow-50 text-yellow-800 border-yellow-200">
                                {machine.expiredFood} expired
                              </Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="w-full bg-gray-200 rounded-full h-2.5 w-24">
                            <div 
                              className="bg-green-600 h-2.5 rounded-full" 
                              style={{ width: `${machine.availableSpace}%` }}
                            ></div>
                          </div>
                          <span className="text-xs text-gray-500">{machine.availableSpace}%</span>
                        </TableCell>
                        <TableCell>
                          <span className="text-xs text-gray-500">
                            {new Date(machine.lastUpdated).toLocaleString()}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">Details</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Add New Machine</Button>
              <Button variant="outline">Export Data</Button>
            </CardFooter>
          </Card>
        </TabsContent>
        
        {/* Volunteers Tab */}
        <TabsContent value="volunteers">
          <Card>
            <CardHeader>
              <CardTitle>Volunteer Management</CardTitle>
              <CardDescription>
                Manage volunteers and their machine assignments.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-700 mx-auto mb-4"></div>
                  <p>Loading volunteer data...</p>
                </div>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Assigned Machines</TableHead>
                      <TableHead>Last Activity</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {volunteers.map(volunteer => (
                      <TableRow key={volunteer.id}>
                        <TableCell className="font-medium">{volunteer.name}</TableCell>
                        <TableCell>{volunteer.email}</TableCell>
                        <TableCell>
                          {volunteer.status === 'active' ? (
                            <Badge className="bg-green-500">Active</Badge>
                          ) : (
                            <Badge className="bg-gray-500">Inactive</Badge>
                          )}
                        </TableCell>
                        <TableCell>
                          {volunteer.assignedMachines.length > 0 ? (
                            <Badge variant="outline">
                              {volunteer.assignedMachines.length} machines
                            </Badge>
                          ) : (
                            <span className="text-gray-500 text-sm">None</span>
                          )}
                        </TableCell>
                        <TableCell>
                          <span className="text-xs text-gray-500">
                            {new Date(volunteer.lastActivity).toLocaleString()}
                          </span>
                        </TableCell>
                        <TableCell>
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm">Edit</Button>
                            <Button variant="outline" size="sm">Assign</Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">Add New Volunteer</Button>
              <Button variant="outline">Send Notifications</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Alerts Section */}
      <Card className="mb-8">
        <CardHeader className="bg-yellow-50">
          <CardTitle className="flex items-center text-yellow-800">
            <AlertTriangle className="h-5 w-5 mr-2" />
            System Alerts
          </CardTitle>
        </CardHeader>
        <CardContent className="pt-4">
          {stats.expiredFoodItems > 0 ? (
            <div className="space-y-4">
              <div className="flex items-start p-3 bg-yellow-50 rounded-md">
                <AlertTriangle className="h-5 w-5 text-yellow-600 mr-3 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800">Expired Food Alert</h4>
                  <p className="text-sm text-yellow-700">
                    {stats.expiredFoodItems} food items have expired and need to be removed from the system.
                  </p>
                  <Button size="sm" className="mt-2 bg-yellow-600 hover:bg-yellow-700">
                    Notify Volunteers
                  </Button>
                </div>
              </div>
              
              {machines.some(m => m.status === 'offline') && (
                <div className="flex items-start p-3 bg-red-50 rounded-md">
                  <AlertTriangle className="h-5 w-5 text-red-600 mr-3 mt-0.5" />
                  <div>
                    <h4 className="font-medium text-red-800">Offline Machines</h4>
                    <p className="text-sm text-red-700">
                      {machines.filter(m => m.status === 'offline').length} machines are currently offline and require attention.
                    </p>
                    <Button size="sm" className="mt-2 bg-red-600 hover:bg-red-700">
                      View Details
                    </Button>
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center py-8">
              <CheckCircle className="h-8 w-8 text-green-500 mr-3" />
              <p className="text-green-700 font-medium">All systems operational. No alerts at this time.</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AdminDashboard;
