
import React from "react";
import { Outlet } from "react-router-dom";
import ConnectionStatus from "./ConnectionStatus";

const CustomerLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-promptBlue text-white flex justify-between items-center p-4">
        <h1 className="text-xl font-medium">Prompt Builder</h1>
        <div className="flex items-center gap-4">
          <ConnectionStatus />
          <div className="bg-promptBlue-500/30 px-3 py-1 rounded-full text-sm">
            Kundtjänst
          </div>
        </div>
      </header>
      <main className="flex-1 p-6 bg-gray-50">
        <Outlet />
      </main>
    </div>
  );
};

export default CustomerLayout;
