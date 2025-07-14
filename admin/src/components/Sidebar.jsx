import React from "react";
import { NavLink } from "react-router-dom";
import { assets } from "../assets/assets";

const Sidebar = () => {
  return (
    <div className="w-[18%] min-h-screen border-r-2 flex flex-col items-start p-4">
      <div className="flex flex-col gap-4 w-full">
        <NavLink
          to="/add"
          className="flex items-center gap-3 border border-gray-500 px-3 py-2 rounded-lg bg-gray-200"
        >
          <img className="w-6 h-6" src={assets.add_icon} alt="Add Items" />
          <p className="text-lg font-semibold hidden md:block">Add Items</p>
        </NavLink>
        <NavLink
          to="/list"
          className="flex items-center gap-3 border border-gray-500 px-3 py-2 rounded-lg bg-gray-200"
        >
          <img className="w-6 h-6" src={assets.parcel_icon} alt="List Items" />
          <p className="text-lg font-semibold hidden md:block">List Items</p>
        </NavLink>
        <NavLink
          to="/orders"
          className="flex items-center gap-3 border border-gray-500 px-3 py-2 rounded-lg bg-gray-200"
        >
          <img className="w-6 h-6" src={assets.order_icon} alt="View Orders" />
          <p className="text-lg font-semibold hidden md:block">View Orders</p>
        </NavLink>
        <NavLink
          to="/stats"
          className="flex items-center gap-3 border border-gray-500 px-3 py-2 rounded-lg bg-gray-200"
        >
          <img className="w-6 h-6" src={assets.image} alt="Stats" />
          <p className="text-lg font-semibold hidden md:block">View Stats</p>
        </NavLink>
      </div>
    </div>
  );
};

export default Sidebar;
