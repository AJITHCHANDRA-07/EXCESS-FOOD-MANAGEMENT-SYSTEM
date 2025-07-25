import React, { useState, useEffect } from 'react';
import { 
  Calendar, 
  Clock, 
  MapPin, 
  CheckCircle2, 
  AlertTriangle,
  ClipboardList
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
  expiredFood: number;
  lastUpdated: string;
}

interface Task {
  id: string;
  machineId: string;
  machineName: string;
  machineAddress: string;
  taskType: 'expired_removal' | 'maintenance' | 'cleaning';
  status: 'pending' | 'in_progress' | 'completed';
  createdAt: string;
  completedAt?: string;
}

interface ActivityLog {
  id: string;
  volunteerId: string;
  machineId: string;
  machineName: string;
  activityType: string;
  timestamp: string;
  details: string;
}

const VolunteerPortal: React.FC = () => {
  const [machines, setMachines] = useState<Machine[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activityLogs, setActivityLogs] = useState<ActivityLog[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [volunteerName, setVolunteerName] = useState<string>('Jane Doe'); // Would come from auth

  // Fetch volunteer data
  useEffect(() => {
    const fetchVolunteerData = async () => {
      setLoading(true);
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data
        const mockMachines: Machine[] = [
          {
            id: 'm1',
            name: 'Downtown Machine',
            address: '123 Main St, Downtown',
            status: 'operational',
            expiredFood: 0,
            lastUpdated: '2025-05-16T08:30:00Z'
          },
          {
            id: 'm2',
            name: 'Westside Machine',
            address: '456 Ocean Ave, Westside',
            status: 'operational',
            expiredFood: 2,
            lastUpdated: '2025-05-16T09:15:00Z'
          },
          {
            id: 'm4',
            name: 'Northside Machine',
            address: '101 Hill St, Northside',
            status: 'operational',
            expiredFood: 3,
            lastUpdated: '2025-05-16T10:00:00Z'
          }
        ];
        
        const mockTasks: Task[] = [
          {
            id: 't1',
            machineId: 'm2',
            machineName: 'Westside Machine',
            machineAddress: '456 Ocean Ave, Westside',
            taskType: 'expired_removal',
            status: 'pending',
            createdAt: '2025-05-16T09:20:00Z'
          },
          {
            id: 't2',
            machineId: 'm4',
            machineName: 'Northside Machine',
            machineAddress: '101 Hill St, Northside',
            taskType: 'expired_removal',
            status: 'pending',
            createdAt: '2025-05-16T10:05:00Z'
          },
          {
            id: 't3',
            machineId: 'm1',
            machineName: 'Downtown Machine',
            machineAddress: '123 Main St, Downtown',
            taskType: 'cleaning',
            status: 'completed',
            createdAt: '2025-05-15T14:30:00Z',
            completedAt: '2025-05-15T15:45:00Z'
          }
        ];
        
        const mockActivityLogs: ActivityLog[] = [
          {
            id: 'a1',
            volunteerId: 'v1',
            machineId: 'm1',
            machineName: 'Downtown Machine',
            activityType: 'cleaning',
            timestamp: '2025-05-15T15:45:00Z',
            details: 'Performed regular cleaning and sanitization.'
          },
          {
            id: 'a2',
            volunteerId: 'v1',
            machineId: 'm3',
            machineName: 'Eastside Machine',
            activityType: 'expired_removal',
            timestamp: '2025-05-14T11:20:00Z',
            details: 'Removed 4 expired food items.'
          },
          {
            id: 'a3',
            volunteerId: 'v1',
            machineId: 'm5',
            machineName: 'Southside Machine',
            activityType: 'maintenance',
            timestamp: '2025-05-12T09:15:00Z',
            details: 'Assisted technician with door mechanism repair.'
          }
        ];
        
        setMachines(mockMachines);
        setTasks(mockTasks);
        setActivityLogs(mockActivityLogs);
      } catch (error) {
        console.error('Error fetching volunteer data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchVolunteerData();
  }, []);

  const handleTaskStatusChange = (taskId: string, newStatus: 'in_progress' | 'completed') => {
    // Update task status
    setTasks(prevTasks => 
      prevTasks.map(task => 
        task.id === taskId 
          ? { ...task, status: newStatus, completedAt: newStatus === 'completed' ? new Date().toISOString() : undefined } 
          : task
      )
    );
    
    // In a real app, this would also make an API call to update the backend
  };

  const getPendingTasks = () => tasks.filter(task => task.status === 'pending');
  const getInProgressTasks = () => tasks.filter(task => task.status === 'in_progress');
  const getCompletedTasks = () => tasks.filter(task => task.status === 'completed');

  const getTaskTypeBadge = (taskType: string) => {
    switch (taskType) {
      case 'expired_removal':
        return <Badge className="bg-yellow-500">Expired Food Removal</Badge>;
      case 'maintenance':
        return <Badge className="bg-blue-500">Maintenance</Badge>;
      case 'cleaning':
        return <Badge className="bg-green-500">Cleaning</Badge>;
      default:
        return <Badge>Other</Badge>;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-green-700">Volunteer Portal</h1>
          <p className="text-gray-600">Welcome back, {volunteerName}</p>
        </div>
        <Button>
          <Calendar className="h-4 w-4 mr-2" />
          Schedule Availability
        </Button>
      </div>

      {/* Tasks Overview */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center">
            <ClipboardList className="h-5 w-5 mr-2" />
            Your Tasks
          </CardTitle>
          <CardDescription>
            Tasks assigned to you that require attention.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-700 mx-auto mb-4"></div>
              <p>Loading tasks...</p>
            </div>
          ) : getPendingTasks().length === 0 && getInProgressTasks().length === 0 ? (
            <div className="flex items-center justify-center py-8">
              <CheckCircle2 className="h-8 w-8 text-green-500 mr-3" />
              <p className="text-green-700 font-medium">No pending tasks at this time. Great job!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {getInProgressTasks().map(task => (
                <Card key={task.id} className="bg-blue-50 border-blue-200">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-lg text-blue-800">{task.machineName}</CardTitle>
                      {getTaskTypeBadge(task.taskType)}
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div className="flex items-start mb-2">
                      <MapPin className="h-4 w-4 text-gray-500 mr-2 mt-0.5" />
                      <span className="text-sm text-gray-700">{task.machineAddress}</span>
                    </div>
                    <div className="flex items-start">
                      <Clock className="h-4 w-4 text-gray-500 mr-2 mt-0.5" />
                      <span className="text-sm text-gray-700">Started: {formatDate(task.createdAt)}</span>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button 
                      className="w-full bg-blue-600 hover:bg-blue-700"
                      onClick={() => handleTaskStatusChange(task.id, 'completed')}
                    >
                      Mark as Completed
                    </Button>
                  </CardFooter>
                </Card>
              ))}
              
              {getPendingTasks().map(task => (
                <Card key={task.id} className="bg-yellow-50 border-yellow-200">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-lg text-yellow-800">{task.machineName}</CardTitle>
                      {getTaskTypeBadge(task.taskType)}
                    </div>
                  </CardHeader>
                  <CardContent className="pb-2">
                    <div className="flex items-start mb-2">
                      <MapPin className="h-4 w-4 text-gray-500 mr-2 mt-0.5" />
                      <span className="text-sm text-gray-700">{task.machineAddress}</span>
                    </div>
                    <div className="flex items-start">
                      <Clock className="h-4 w-4 text-gray-500 mr-2 mt-0.5" />
                      <span className="text-sm text-gray-700">Created: {formatDate(task.createdAt)}</span>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button 
                      className="w-full bg-yellow-600 hover:bg-yellow-700"
                      onClick={() => handleTaskStatusChange(task.id, 'in_progress')}
                    >
                      Start Task
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
      <Tabs defaultValue="machines" className="mb-8">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="machines">Assigned Machines</TabsTrigger>
          <TabsTrigger value="activity">Activity Log</TabsTrigger>
        </TabsList>
        
        {/* Machines Tab */}
        <TabsContent value="machines">
          <Card>
            <CardHeader>
              <CardTitle>Your Assigned Machines</CardTitle>
              <CardDescription>
                Machines you are responsible for maintaining.
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
                      <TableHead>Expired Food</TableHead>
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
                        <TableCell>
                          {machine.status === 'operational' ? (
                            <Badge className="bg-green-500">Operational</Badge>
                          ) : machine.status === 'maintenance' ? (
                            <Badge className="bg-yellow-500">Maintenance</Badge>
                          ) : (
                            <Badge className="bg-red-500">Offline</Badge>
                          )}
                        </TableCell>
                        <TableCell>
                          {machine.expiredFood > 0 ? (
                            <Badge variant="outline" className="bg-yellow-50 text-yellow-800 border-yellow-200">
                              {machine.expiredFood} items
                            </Badge>
                          ) : (
                            <span className="text-green-600 text-sm">None</span>
                          )}
                        </TableCell>
                        <TableCell>
                          <span className="text-xs text-gray-500">
                            {formatDate(machine.lastUpdated)}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Button variant="outline" size="sm">View Details</Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </TabsContent>
        
        {/* Activity Log Tab */}
        <TabsContent value="activity">
          <Card>
            <CardHeader>
              <CardTitle>Your Activity History</CardTitle>
              <CardDescription>
                Record of your recent activities and tasks.
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-700 mx-auto mb-4"></div>
                  <p>Loading activity data...</p>
                </div>
              ) : activityLogs.length === 0 ? (
                <div className="text-center py-8 bg-gray-50 rounded-lg">
                  <p className="text-gray-500">No activity records found.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {activityLogs.map(log => (
                    <div key={log.id} className="border-l-4 border-green-500 pl-4 py-2">
                      <div className="flex justify-between items-start">
                        <h4 className="font-medium">{log.activityType}</h4>
                        <span className="text-xs text-gray-500">{formatDate(log.timestamp)}</span>
                      </div>
                      <p className="text-sm text-gray-700 mb-1">{log.details}</p>
                      <div className="flex items-center">
                        <MapPin className="h-3 w-3 text-gray-400 mr-1" />
                        <span className="text-xs text-gray-500">{log.machineName}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
            <CardFooter>
              <Button variant="outline" className="w-full">View All Activity</Button>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Alerts Section */}
      {machines.some(m => m.expiredFood > 0) && (
        <Card className="mb-8">
          <CardHeader className="bg-yellow-50">
            <CardTitle className="flex items-center text-yellow-800">
              <AlertTriangle className="h-5 w-5 mr-2" />
              Attention Required
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-4">
            <div className="flex items-start p-3 bg-yellow-50 rounded-md">
              <AlertTriangle className="h-5 w-5 text-yellow-600 mr-3 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800">Expired Food Alert</h4>
                <p className="text-sm text-yellow-700">
                  {machines.reduce((total, m) => total + m.expiredFood, 0)} food items have expired and need to be removed.
                </p>
                <Button size="sm" className="mt-2 bg-yellow-600 hover:bg-yellow-700">
                  View Tasks
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default VolunteerPortal;
