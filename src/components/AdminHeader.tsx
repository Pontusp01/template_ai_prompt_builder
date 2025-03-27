
import React from "react";
import ConnectionStatus from "./ConnectionStatus";

interface AdminHeaderProps {
  title?: string;
}

const AdminHeader: React.FC<AdminHeaderProps> = ({ title }) => {
  return (
    <header className="bg-promptBlue text-white flex justify-between items-center p-4">
      <h1 className="text-xl font-medium">{title || "Prompt Builder Admin"}</h1>
      <div className="flex items-center gap-4">
        <ConnectionStatus />
        <div className="bg-promptBlue-500/30 px-3 py-1 rounded-full text-sm">
          Admin (SSO)
        </div>
      </div>
    </header>
  );
};

export default AdminHeader;
