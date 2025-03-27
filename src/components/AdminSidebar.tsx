
import React from "react";
import { NavLink } from "react-router-dom";
import {
  BarChart3,
  Mail,
  LayoutGrid,
  ClipboardList,
  FileText,
  Settings
} from "lucide-react";

const AdminSidebar: React.FC = () => {
  const navItems = [
    { icon: BarChart3, label: "Dashboard", path: "/admin" },
    { icon: Mail, label: "Mallar", path: "/admin/templates" },
    { icon: LayoutGrid, label: "Avdelningar", path: "/admin/departments" },
    { icon: ClipboardList, label: "Kompletteringstyper", path: "/admin/completion-types" },
    { icon: FileText, label: "Texthantering", path: "/admin/text-management" },
    { icon: Settings, label: "Inställningar", path: "/admin/settings" }
  ];

  return (
    <div className="bg-promptBlue w-[220px] min-h-screen flex flex-col py-4">
      <div className="px-4 py-3">
        <h1 className="text-xl font-medium text-white">Prompt Builder Admin</h1>
      </div>
      
      <div className="px-4 py-3 mt-4">
        <p className="text-white/70 uppercase text-xs font-semibold tracking-wider mb-3">Huvudmeny</p>
        <nav className="space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => 
                `admin-nav-item ${isActive ? "active" : ""}`
              }
            >
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default AdminSidebar;
