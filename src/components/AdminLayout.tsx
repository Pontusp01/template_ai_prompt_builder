
import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import AdminSidebar from "./AdminSidebar";
import AdminHeader from "./AdminHeader";

const AdminLayout: React.FC = () => {
  const location = useLocation();
  
  // Determine the page title based on the current route
  const getPageTitle = () => {
    const path = location.pathname;
    if (path === "/admin" || path === "/admin/") return "Dashboard";
    if (path.includes("/admin/templates")) return "Templates";
    if (path.includes("/admin/departments")) return "Departments";
    if (path.includes("/admin/completion-types")) return "Completion Types";
    if (path.includes("/admin/text-management")) return "Text Management";
    if (path.includes("/admin/settings")) return "Settings";
    return "Prompt Builder Admin";
  };

  return (
    <div className="flex min-h-screen">
      <AdminSidebar />
      <div className="flex-1 flex flex-col">
        <AdminHeader title={getPageTitle()} />
        <main className="flex-1 p-6 bg-gray-50">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
