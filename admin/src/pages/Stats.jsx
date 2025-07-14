import React from "react";
import { useNavigate } from "react-router-dom";

const Stats = () => {
  const navigate = useNavigate();

  const statsData = [
    {
      title: "Fraud Detection",
      value: "23 Reports",
      description: "Flagged transactions in last 30 days",
      color: "bg-red-100",
      route: "/stats/frauds",
    },
    {
      title: "Carbon Footprint",
      value: "1340 kg CO₂",
      description: "Monthly footprint from logistics",
      color: "bg-green-100",
      route: "/stats/carbon",
    },
    {
      title: "Reverse Logistics",
      value: "87 Returns",
      description: "Optimized reverse shipments this month",
      color: "bg-yellow-100",
      route: "/stats/reverse-logistics",
    },
    {
      title: "Agentic AI Usage",
      value: "1.2k Queries",
      description: "Total AI queries served this month",
      color: "bg-blue-100",
      route: "/stats/agentic-ai",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6">
      {statsData.map((stat, index) => (
        <div
          key={index}
          className={`p-6 rounded-xl shadow-md cursor-pointer ${stat.color} hover:scale-105 transition-transform`}
          onClick={() => navigate(stat.route)}
        >
          <h2 className="text-xl font-semibold text-gray-800">{stat.title}</h2>
          <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
          <p className="text-sm text-gray-600 mt-1">{stat.description}</p>
        </div>
      ))}
    </div>
  );
};

export default Stats;
