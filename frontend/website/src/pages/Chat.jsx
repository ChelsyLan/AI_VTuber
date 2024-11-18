import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { collection, getDocs, query, where } from "firebase/firestore";
import { db } from "../firebase";

export default function Chat() {
  const [liveData, setLiveData] = useState({ live_link: null, name: null, chat_link: null });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchLiveData() {
      try {
        // Reference to the aiAgents collection
        const agentsRef = collection(db, "aiAgents");
        const q = query(agentsRef, where("campaignId", "==", "1"));
        const querySnap = await getDocs(q);

        if (!querySnap.empty) {
          const docData = querySnap.docs[0].data();
          setLiveData({ live_link: docData.live_link, name: docData.name, chat_link: docData.chat_link });
        } else {
          toast.error("Campaign not found");
        }
      } catch (error) {
        toast.error("Could not fetch live data");
      } finally {
        setLoading(false);
      }
    }

    fetchLiveData();
  }, []);

  const handleChatNow = () => {
    if (liveData.chat_link) {
      window.open(liveData.chat_link, "_blank");
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-3">
      <h1 className="text-3xl text-center mt-6 font-bold mb-6">
        {"Chat with " + liveData.name || "AI Shopping Streamer Assistant"}
      </h1>
      {loading ? (
        <p>Loading...</p>
      ) : liveData.live_link ? (
        <div className="flex flex-col items-center">
          <div className="relative w-full" style={{ paddingTop: "56.25%" }}>
            <iframe
              className="absolute top-0 left-0 w-full h-full"
              src={liveData.live_link}
              title={liveData.name || "YouTube Live Stream"}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              allowFullScreen
            ></iframe>
          </div>
          <button
            onClick={handleChatNow}
            className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition duration-150"
          >
            Chat Now
          </button>
        </div>
      ) : (
        <p>SORRY OUR AI VTUBER IS CURRENTLY OFFLINE {liveData.name}</p>
      )}
    </div>
  );
}
