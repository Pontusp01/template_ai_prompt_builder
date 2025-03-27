
import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3, Users, FileText } from "lucide-react";

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-promptLightBlue border-none">
          <CardContent className="p-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-500">Totalt antal mallar</p>
                <h3 className="text-3xl font-bold text-promptBlue mt-1">12</h3>
                <p className="text-xs text-green-600 mt-1">+2 från förra månaden</p>
              </div>
              <div className="h-12 w-12 bg-promptBlue-100 rounded-full flex items-center justify-center">
                <FileText className="h-6 w-6 text-promptBlue" />
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-green-50 border-none">
          <CardContent className="p-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-500">Aktiva användare</p>
                <h3 className="text-3xl font-bold text-green-600 mt-1">28</h3>
                <p className="text-xs text-green-600 mt-1">+5 från förra månaden</p>
              </div>
              <div className="h-12 w-12 bg-green-100 rounded-full flex items-center justify-center">
                <Users className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-amber-50 border-none">
          <CardContent className="p-6">
            <div className="flex justify-between items-center">
              <div>
                <p className="text-sm text-gray-500">Skapade prompter</p>
                <h3 className="text-3xl font-bold text-amber-600 mt-1">487</h3>
                <p className="text-xs text-green-600 mt-1">+112 från förra månaden</p>
              </div>
              <div className="h-12 w-12 bg-amber-100 rounded-full flex items-center justify-center">
                <BarChart3 className="h-6 w-6 text-amber-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Populära mallar</CardTitle>
            <p className="text-sm text-gray-500">Baserat på användning senaste 30 dagarna</p>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm">Reseinformation</span>
                <div className="w-48 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-200 rounded-full" 
                    style={{ width: '80%' }}
                  ></div>
                </div>
                <span className="text-sm font-medium">186</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Klagomålshantering</span>
                <div className="w-48 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-green-400 rounded-full" 
                    style={{ width: '65%' }}
                  ></div>
                </div>
                <span className="text-sm font-medium">148</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Ersättningsärenden</span>
                <div className="w-48 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-blue-400 rounded-full" 
                    style={{ width: '50%' }}
                  ></div>
                </div>
                <span className="text-sm font-medium">116</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Allmän information</span>
                <div className="w-48 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-amber-400 rounded-full" 
                    style={{ width: '40%' }}
                  ></div>
                </div>
                <span className="text-sm font-medium">94</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm">Förseningsinfo</span>
                <div className="w-48 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-purple-400 rounded-full" 
                    style={{ width: '30%' }}
                  ></div>
                </div>
                <span className="text-sm font-medium">70</span>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle>Senaste aktiviteter</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center text-sm">
                <span>Ny mall skapad: "Förseningsinfo"</span>
                <span className="text-gray-500">2023-03-24 14:30</span>
              </div>
              <div className="border-t pt-4 flex justify-between items-center text-sm">
                <span>Mall redigerad: "Reseinformation"</span>
                <span className="text-gray-500">2023-03-23 09:45</span>
              </div>
              <div className="border-t pt-4 flex justify-between items-center text-sm">
                <span>Ny avdelning skapad: "Kvalitet"</span>
                <span className="text-gray-500">2023-03-22 16:15</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
