import React from "react";

const reverseData = [
  {
    id: 1,
    title: "Product A",
    productId: "SKU-001A",
    customerName: "Alice Johnson",
    location: "New York, USA",
    returnDate: "2025-07-11",
    timesReturned: 12,
    reason: "Size mismatch",
  },
  {
    id: 2,
    title: "Product B",
    productId: "SKU-002B",
    customerName: "Ravi Mehta",
    location: "Delhi, India",
    returnDate: "2025-07-10",
    timesReturned: 9,
    reason: "Color variation issue",
  },
  {
    id: 3,
    title: "Product C",
    productId: "SKU-003C",
    customerName: "Sophia Lin",
    location: "Shanghai, China",
    returnDate: "2025-07-09",
    timesReturned: 7,
    reason: "Defective batch",
  },
  {
    id: 4,
    title: "Product D",
    productId: "SKU-004D",
    customerName: "Daniel Smith",
    location: "London, UK",
    returnDate: "2025-07-08",
    timesReturned: 6,
    reason: "Customer remorse",
  },
  {
    id: 5,
    title: "Product E",
    productId: "SKU-005E",
    customerName: "Lara Mendes",
    location: "Sao Paulo, Brazil",
    returnDate: "2025-07-07",
    timesReturned: 5,
    reason: "Late delivery",
  },
  {
    id: 6,
    title: "Product F",
    productId: "SKU-006F",
    customerName: "Chris Adams",
    location: "Chicago, USA",
    returnDate: "2025-07-06",
    timesReturned: 10,
    reason: "Poor material quality",
  },
  {
    id: 7,
    title: "Product G",
    productId: "SKU-007G",
    customerName: "Fatima Noor",
    location: "Dubai, UAE",
    returnDate: "2025-07-05",
    timesReturned: 4,
    reason: "Wrong item sent",
  },
  {
    id: 8,
    title: "Product H",
    productId: "SKU-008H",
    customerName: "Kenji Watanabe",
    location: "Osaka, Japan",
    returnDate: "2025-07-04",
    timesReturned: 3,
    reason: "Damage in transit",
  },
  {
    id: 9,
    title: "Product I",
    productId: "SKU-009I",
    customerName: "Chen Wei",
    location: "Beijing, China",
    returnDate: "2025-07-03",
    timesReturned: 8,
    reason: "Duplicate item issue",
  },
  {
    id: 10,
    title: "Product J",
    productId: "SKU-010J",
    customerName: "Olivia Brown",
    location: "Sydney, Australia",
    returnDate: "2025-07-02",
    timesReturned: 2,
    reason: "Inaccurate listing",
  },
  {
    id: 11,
    title: "Product K",
    productId: "SKU-011K",
    customerName: "Ahmed Hassan",
    location: "Cairo, Egypt",
    returnDate: "2025-07-01",
    timesReturned: 6,
    reason: "Accessories missing",
  },
  {
    id: 12,
    title: "Product L",
    productId: "SKU-012L",
    customerName: "Emma Green",
    location: "Toronto, Canada",
    returnDate: "2025-06-30",
    timesReturned: 7,
    reason: "Packaging damaged",
  },
  {
    id: 13,
    title: "Product M",
    productId: "SKU-013M",
    customerName: "George Clark",
    location: "Berlin, Germany",
    returnDate: "2025-06-29",
    timesReturned: 5,
    reason: "Item expired",
  },
];

const ReverseLogisticsStats = () => {
  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {reverseData.map((item) => (
        <div key={item.id} className="bg-yellow-50 p-4 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-yellow-800">{item.title}</h3>
          <p className="text-sm text-gray-600"><strong>SKU:</strong> {item.productId}</p>
          <p className="text-sm text-gray-600"><strong>Customer:</strong> {item.customerName}</p>
          <p className="text-sm text-gray-600"><strong>Location:</strong> {item.location}</p>
          <p className="text-sm text-gray-600"><strong>Return Date:</strong> {item.returnDate}</p>
          <p className="text-sm text-gray-600"><strong>Times Returned:</strong> {item.timesReturned}</p>
          <p className="text-sm text-gray-700 mt-2"><strong>Reason:</strong> {item.reason}</p>
        </div>
      ))}
    </div>
  );
};

export default ReverseLogisticsStats;
