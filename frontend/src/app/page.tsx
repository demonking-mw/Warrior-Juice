
import { LatestPost } from "~/app/_components/post";
import { api, HydrateClient } from "~/trpc/server";

export default async function Home() {
  const hello = await api.post.hello({ text: "WarriorJuice" });

  void api.post.getLatest.prefetch();

  return (
    <HydrateClient>
      <main className="flex min-h-screen flex-col justify-center bg-gradient-to-b from-[#FAE100] to-[#EAAB00] text-black">
        <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16">
          <h1 className="text-5xl font-extrabold items-center tracking-tight sm:text-[5rem]">
          Warrior<span className="text-[#EF60AD]">Juice</span>
          </h1>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-8">
        <div className="flex max-w-xs flex-col gap-4 bg-white/10 p-4 hover:bg-white/20">
          <h3 className="text-2xl font-bold">All About Juice</h3>
          <div className="text-lg">
            Juice is the liquid obtained from or present in fruit or vegetables.
      </div>
        </div>
        <LatestPost />
        </div>
        <div className="flex flex-col items-center gap-2">
          <p className="text-2xl text-white">
            {hello ? hello.greeting : "Loading tRPC query..."}
          </p>
          </div>
        </div>
      </main>
    </HydrateClient>
  );
}
