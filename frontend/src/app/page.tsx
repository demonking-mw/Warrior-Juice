import Link from "next/link";

import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";
export default async function Home() {

  

  void api.post.getLatest.prefetch();

  return (
    <div className="flex flex-col items-center space-y-4">
      <div>
        <div className="p-4 rounded-md">
          <h1 className="font-bold text-center">Welcome to Warrior Juice</h1>
        </div>
        
        <p>
          This is a blog where you can find all the latest news and updates
          about the game Warrior Juice.
        </p>
        <div className="p-4 items-center space-y-4">
          <p>
            <Link href="/auth">Go to login</Link>
        </p>
        </div>
        
      </div>
    </div>
  );
}
