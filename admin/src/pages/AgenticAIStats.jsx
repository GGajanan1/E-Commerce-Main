import React from "react";

const aiData = [
  {
    id: 1,
    metric: "Query Volume",
    value: "1245 queries",
    user: "All Users",
    timestamp: "July 12, 2025",
    impact: "Indicates consistent daily usage across customer support.",
    details: "1245 queries processed this month.",
  },
  {
    id: 2,
    metric: "Multilingual Support",
    value: "4 languages",
    user: "Global Audience",
    timestamp: "July 10, 2025",
    impact: "Enhanced accessibility for international users.",
    details: "Supports English, Hindi, Spanish, French.",
  },
  {
    id: 3,
    metric: "Average Response Time",
    value: "1.24 sec",
    user: "All Sessions",
    timestamp: "July 12, 2025",
    impact: "Maintains fast interaction speed.",
    details: "1.24 seconds per response.",
  },
  {
    id: 4,
    metric: "Peak Load",
    value: "300 queries/hr",
    user: "Sale Day Users",
    timestamp: "July 05, 2025",
    impact: "Handled high concurrency during flash sales.",
    details: "300 queries/hour during sale.",
  },
  {
    id: 5,
    metric: "Top Use Case",
    value: "Order Tracking",
    user: "Frequent Shoppers",
    timestamp: "July 08, 2025",
    impact: "Majority ask about orders and refunds.",
    details: "Most queries are about order status and refund tracking.",
  },
  {
    id: 6,
    metric: "Intent Detection Accuracy",
    value: "97.3%",
    user: "Test Group A",
    timestamp: "July 06, 2025",
    impact: "Shows high precision in understanding customer intent.",
    details: "97.3% accuracy based on test set.",
  },
  {
    id: 7,
    metric: "User Rating",
    value: "4.7/5",
    user: "350 respondents",
    timestamp: "July 11, 2025",
    impact: "Excellent satisfaction rating from users.",
    details: "Average rating 4.7/5 from 350 users.",
  },
  {
    id: 8,
    metric: "Feedback Collected",
    value: "94% positive",
    user: "All Sessions",
    timestamp: "July 10, 2025",
    impact: "Majority found the bot helpful.",
    details: "94% users rated the bot as helpful.",
  },
  {
    id: 9,
    metric: "Escalation Rate",
    value: "3.5%",
    user: "Customer Support",
    timestamp: "July 09, 2025",
    impact: "Low human intervention required.",
    details: "Only 3.5% of queries needed human handoff.",
  },
  {
    id: 10,
    metric: "Product Suggestions",
    value: "12.4% CTR",
    user: "Returning Users",
    timestamp: "July 11, 2025",
    impact: "Bot is effectively driving product discovery.",
    details: "Suggested products clicked 12.4% of the time.",
  },
  {
    id: 11,
    metric: "Context Retention",
    value: "Enabled",
    user: "Multi-turn Sessions",
    timestamp: "July 08, 2025",
    impact: "Bot remembers session context for smoother interaction.",
    details: "Session-aware queries supported.",
  },
  {
    id: 12,
    metric: "Bot Downtime",
    value: "0.5%",
    user: "All Users",
    timestamp: "July 01–31, 2025",
    impact: "Very high reliability and uptime.",
    details: "Only 0.5% downtime last month.",
  },
  {
    id: 13,
    metric: "Security Audits",
    value: "Passed",
    user: "Internal QA",
    timestamp: "July 07, 2025",
    impact: "All privacy and compliance checks passed.",
    details: "Passed all internal privacy and security audits.",
  },
];

const AgenticAIStats = () => {
  return (
    <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {aiData.map((item) => (
        <div key={item.id} className="bg-blue-50 p-4 rounded-xl shadow-md">
          <h3 className="text-lg font-bold text-blue-800">{item.metric}</h3>
          <p className="text-sm text-gray-600"><strong>Value:</strong> {item.value}</p>
          <p className="text-sm text-gray-600"><strong>User:</strong> {item.user}</p>
          <p className="text-sm text-gray-600"><strong>Last Updated:</strong> {item.timestamp}</p>
          <p className="text-sm text-gray-700 mt-2"><strong>Insight:</strong> {item.impact}</p>
          <p className="text-sm text-gray-700 mt-1">{item.details}</p>
        </div>
      ))}
    </div>
  );
};

export default AgenticAIStats;
