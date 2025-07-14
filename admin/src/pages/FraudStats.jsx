import React from "react";

const fraudData = [
  {
    id: 1,
    title: "Suspicious Payment",
    name: "John Doe",
    location: "New York, USA",
    transactionId: "TXN101A",
    mode: "Credit Card",
    cost: "$1200",
    details: "Card used in multiple regions in a short span.",
  },
  {
    id: 2,
    title: "IP Mismatch",
    name: "Amit Kumar",
    location: "Mumbai, India / Berlin, Germany",
    transactionId: "TXN102B",
    mode: "Netbanking",
    cost: "$560",
    details: "Login and payment locations don't match.",
  },
  {
    id: 3,
    title: "Bulk Returns Abuse",
    name: "Sophia Li",
    location: "Shanghai, China",
    transactionId: "TXN103C",
    mode: "UPI",
    cost: "$89",
    details: "Returned 90%+ of orders over last 60 days.",
  },
  {
    id: 4,
    title: "Invalid Promo Use",
    name: "David Smith",
    location: "London, UK",
    transactionId: "TXN104D",
    mode: "Debit Card",
    cost: "$140",
    details: "Promo code reused beyond allowed limit.",
  },
  {
    id: 5,
    title: "High Risk BIN",
    name: "Carlos Diaz",
    location: "Mexico City, Mexico",
    transactionId: "TXN105E",
    mode: "Credit Card",
    cost: "$650",
    details: "Card BIN associated with known chargebacks.",
  },
  {
    id: 6,
    title: "High Value Order",
    name: "Emily Clark",
    location: "Toronto, Canada",
    transactionId: "TXN106F",
    mode: "PayPal",
    cost: "$10,000",
    details: "Large transaction from a first-time buyer.",
  },
  {
    id: 7,
    title: "Mismatched Email",
    name: "Fatima Noor",
    location: "Dubai, UAE",
    transactionId: "TXN107G",
    mode: "UPI",
    cost: "$480",
    details: "Email domain didn't match billing address.",
  },
  {
    id: 8,
    title: "VPN Proxy Use",
    name: "Kenji Watanabe",
    location: "Tokyo, Japan",
    transactionId: "TXN108H",
    mode: "Credit Card",
    cost: "$210",
    details: "Anonymized IP detected during checkout.",
  },
  {
    id: 9,
    title: "Frequent Failed Attempts",
    name: "Laura King",
    location: "California, USA",
    transactionId: "TXN109I",
    mode: "Card",
    cost: "$375",
    details: "7 failed payment attempts in one session.",
  },
  {
    id: 10,
    title: "Gift Card Exploit",
    name: "Jorge Silva",
    location: "Lisbon, Portugal",
    transactionId: "TXN110J",
    mode: "Gift Card",
    cost: "$95",
    details: "Suspicious bulk redemption of gift cards.",
  },
  {
    id: 11,
    title: "Billing/Shipping Mismatch",
    name: "Chen Wei",
    location: "Beijing, China",
    transactionId: "TXN111K",
    mode: "Netbanking",
    cost: "$130",
    details: "Shipping address differs significantly from billing.",
  },
  {
    id: 12,
    title: "Fake Reviews",
    name: "Olivia Brown",
    location: "Sydney, Australia",
    transactionId: "TXN112L",
    mode: "Credit Card",
    cost: "$215",
    details: "AI detected unnatural 5-star review activity.",
  },
  {
    id: 13,
    title: "Excessive Account Creation",
    name: "Ahmed Hassan",
    location: "Cairo, Egypt",
    transactionId: "TXN113M",
    mode: "UPI",
    cost: "$72",
    details: "25 accounts created from same IP.",
  },
];

const FraudStats = () => {
  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {fraudData.map((item) => (
        <div key={item.id} className="bg-red-50 p-4 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-red-800">{item.title}</h3>
          <p className="text-sm text-gray-600 mt-1"><strong>Customer:</strong> {item.name}</p>
          <p className="text-sm text-gray-600"><strong>Location:</strong> {item.location}</p>
          <p className="text-sm text-gray-600"><strong>Transaction ID:</strong> {item.transactionId}</p>
          <p className="text-sm text-gray-600"><strong>Payment Mode:</strong> {item.mode}</p>
          <p className="text-sm text-gray-600"><strong>Amount:</strong> {item.cost}</p>
          <p className="text-sm text-gray-700 mt-2">{item.details}</p>
        </div>
      ))}
    </div>
  );
};

export default FraudStats;
