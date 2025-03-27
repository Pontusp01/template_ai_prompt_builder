
import React, { useState, useEffect } from "react";
import { Database, Server } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/integrations/supabase/client";

interface ConnectionStatusProps {
  className?: string;
}

const BACKEND_URL = "http://localhost:5000"; // Python backend URL

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ className }) => {
  const [dbStatus, setDbStatus] = useState<"connected" | "disconnected" | "loading">("loading");
  const [apiStatus, setApiStatus] = useState<"connected" | "disconnected" | "loading">("loading");
  const { toast } = useToast();

  useEffect(() => {
    const checkConnections = async () => {
      // Check direct Supabase connection
      try {
        // Create a dynamically typed client to bypass TypeScript restrictions
        // This is a workaround for tables not present in the TypeScript definitions
        const { data, error } = await (supabase as any).from('colors').select().limit(1);
        
        if (error) {
          console.error("Supabase connection error:", error);
          setDbStatus("disconnected");
          toast({
            title: "Database Connection Issue",
            description: "Cannot connect directly to Supabase. Check your configuration.",
            variant: "destructive",
          });
        } else {
          setDbStatus("connected");
        }
      } catch (error) {
        console.error("Supabase connection error:", error);
        setDbStatus("disconnected");
      }

      // Check Python API connection
      try {
        const apiResponse = await fetch(`${BACKEND_URL}/api/status`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (apiResponse.ok) {
          setApiStatus("connected");
          const data = await apiResponse.json();
          
          // If the API is up but cannot connect to the database
          if (!data.database_connected) {
            toast({
              title: "Backend Database Connection Issue",
              description: "The backend cannot connect to the database. Check your configuration.",
              variant: "destructive",
            });
          }
        } else {
          setApiStatus("disconnected");
          toast({
            title: "Backend Connection Failed",
            description: "Could not connect to the Python backend. Is it running?",
            variant: "destructive",
          });
        }
      } catch (error) {
        console.error("Error checking Python API connection:", error);
        setApiStatus("disconnected");
        
        toast({
          title: "Backend Connection Failed",
          description: "Could not connect to the Python backend. Is it running?",
          variant: "destructive",
        });
      }
    };

    checkConnections();

    // Poll connections periodically
    const interval = setInterval(checkConnections, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, [toast]);

  const getStatusClass = (status: "connected" | "disconnected" | "loading") => {
    if (status === "connected") return "status-connected";
    if (status === "disconnected") return "status-disconnected";
    return "status-loading";
  };

  const getStatusText = (status: "connected" | "disconnected" | "loading") => {
    if (status === "connected") return "Connected";
    if (status === "disconnected") return "Disconnected";
    return "Connecting...";
  };

  return (
    <div className={`flex items-center space-x-4 ${className}`}>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
              <Database className="h-4 w-4" />
              <span className={`status-indicator ${getStatusClass(dbStatus)}`} />
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <p>Database: {getStatusText(dbStatus)}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <div className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-white/10 backdrop-blur-sm">
              <Server className="h-4 w-4" />
              <span className={`status-indicator ${getStatusClass(apiStatus)}`} />
            </div>
          </TooltipTrigger>
          <TooltipContent>
            <p>Python API: {getStatusText(apiStatus)}</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  );
};

export default ConnectionStatus;
