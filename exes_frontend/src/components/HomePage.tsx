import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const HomePage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center text-center py-12 bg-green-50 rounded-lg mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-green-700 mb-4">
          Exes Food Management System
        </h1>
        <p className="text-xl text-gray-700 max-w-3xl mb-8">
          Connecting excess food with those who need it most. Our network of smart machines
          makes donating and receiving food simple, efficient, and accessible.
        </p>
        <div className="flex flex-col sm:flex-row gap-4">
          <Link to="/locate?mode=donor">
            <Button size="lg" className="bg-yellow-500 hover:bg-yellow-600 text-gray-800">
              I Want to Donate Food
            </Button>
          </Link>
          <Link to="/locate?mode=receiver">
            <Button size="lg" className="bg-green-600 hover:bg-green-700 text-white">
              I Need Food
            </Button>
          </Link>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8 text-green-700">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* For Donors */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-yellow-600">For Donors</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>Find a nearby machine with available space</li>
                <li>Input food quantity and expiry date</li>
                <li>Place food in the designated compartment</li>
                <li>Receive confirmation of your donation</li>
              </ol>
            </CardContent>
          </Card>

          {/* For Receivers */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-green-600">For Receivers</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>Find a nearby machine with available food</li>
                <li>Request food from the machine</li>
                <li>Collect food from the designated compartment</li>
                <li>Enjoy your meal!</li>
              </ol>
            </CardContent>
          </Card>

          {/* For Volunteers */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl text-blue-600">For Volunteers</CardTitle>
            </CardHeader>
            <CardContent>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>Sign up as a volunteer</li>
                <li>View machines that need maintenance</li>
                <li>Remove expired food and clean machines</li>
                <li>Help keep the system running smoothly</li>
              </ol>
              <div className="mt-4">
                <Link to="/volunteer/login">
                  <Button variant="outline" className="w-full">Volunteer Login</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* About Section */}
      <section className="mb-16">
        <h2 className="text-3xl font-bold text-center mb-8 text-green-700">About Our Mission</h2>
        <div className="bg-white p-8 rounded-lg shadow-md">
          <p className="text-gray-700 mb-4">
            The Exes Food Management System was created to address two critical issues: food waste and food insecurity.
            By providing a network of smart machines throughout the community, we make it easy for people with excess
            food to donate it anonymously, and for those in need to access it with dignity.
          </p>
          <p className="text-gray-700 mb-4">
            Our system ensures that food is stored safely, tracked for freshness, and distributed efficiently.
            Volunteers help maintain the machines and ensure that expired food is removed promptly.
          </p>
          <p className="text-gray-700">
            Together, we can reduce waste and ensure that good food reaches those who need it most.
          </p>
        </div>
      </section>

      {/* Admin Section */}
      <section className="text-center mb-8">
        <Link to="/admin/login">
          <Button variant="outline" size="sm">Admin Login</Button>
        </Link>
      </section>
    </div>
  );
};

export default HomePage;
