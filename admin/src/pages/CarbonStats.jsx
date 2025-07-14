import React from "react";

const carbonData = [
  {
    id: 1,
    title: "Manufacturing - Product A",
    category: "Manufacturing",
    product: "Product A",
    vehicle: "N/A",
    details: "340 kg CO₂ generated during raw material processing.",
  },
  {
    id: 2,
    title: "Packaging Waste",
    category: "Packaging",
    product: "Product B",
    vehicle: "N/A",
    details: "210 kg CO₂ equivalent waste from plastic and paper materials.",
  },
  {
    id: 3,
    title: "Delivery Trucks (Tier-1)",
    category: "Transportation",
    product: "All Orders",
    vehicle: "Tata LPT 709",
    details: "Estimated 450 kg CO₂ from regional deliveries.",
  },
  {
    id: 4,
    title: "Air Freight",
    category: "Air Logistics",
    product: "Product C",
    vehicle: "Boeing 777 Cargo",
    details: "Carbon output of 620 kg CO₂ from international air cargo.",
  },
  {
    id: 5,
    title: "Electricity Consumption",
    category: "Energy Use",
    product: "Warehouse Ops",
    vehicle: "N/A",
    details: "135 kWh consumed resulting in 102 kg CO₂.",
  },
  {
    id: 6,
    title: "Returns & Repackaging",
    category: "Reverse Logistics",
    product: "Product D",
    vehicle: "Mahindra Loadking",
    details: "122 kg CO₂ created from processing and reshipping returns.",
  },
  {
    id: 7,
    title: "Cold Storage",
    category: "Refrigeration",
    product: "Product E",
    vehicle: "Isuzu Cold Truck",
    details: "Refrigerated transport emitted 89 kg CO₂.",
  },
  {
    id: 8,
    title: "Last-mile bikes (Eco)",
    category: "Green Delivery",
    product: "Small Parcels",
    vehicle: "Electric Bikes",
    details: "Only 10 kg CO₂ generated from local eco-bike fleet.",
  },
  {
    id: 9,
    title: "Server Hosting",
    category: "Digital",
    product: "E-commerce Infra",
    vehicle: "N/A",
    details: "Cloud infrastructure responsible for ~50 kg CO₂.",
  },
  {
    id: 10,
    title: "Employee Commuting",
    category: "HR/Operations",
    product: "Office Ops",
    vehicle: "Mixed (Car/Metro)",
    details: "Hybrid policy saved approx. 180 kg CO₂ this month.",
  },
  {
    id: 11,
    title: "Reverse Shipments",
    category: "Returns",
    product: "Product F",
    vehicle: "Ashok Leyland Dost",
    details: "96 kg CO₂ estimated from pickups and logistics.",
  },
  {
    id: 12,
    title: "Sustainable Products",
    category: "Green Product Line",
    product: "Eco Bag & Bottle",
    vehicle: "N/A",
    details: "Emission reduced by 230 kg CO₂ via eco-design.",
  },
  {
    id: 13,
    title: "Green Partners",
    category: "Logistics",
    product: "Multiple SKUs",
    vehicle: "Delhivery Fleet",
    details: "Partner carrier reduced emissions by 20%.",
  },
];

const CarbonStats = () => {
  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {carbonData.map((item) => (
        <div key={item.id} className="bg-green-50 p-4 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-green-800">{item.title}</h3>
          <p className="text-sm text-gray-600 mt-1"><strong>Category:</strong> {item.category}</p>
          <p className="text-sm text-gray-600"><strong>Product:</strong> {item.product}</p>
          <p className="text-sm text-gray-600"><strong>Vehicle:</strong> {item.vehicle}</p>
          <p className="text-sm text-gray-700 mt-2">{item.details}</p>
        </div>
      ))}
    </div>
  );
};

export default CarbonStats;
