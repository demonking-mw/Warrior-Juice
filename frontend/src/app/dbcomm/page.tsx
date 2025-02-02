import React from "react";

/**
 * playground
 * test for front-back communication or other things
 */

const Page: React.FC = () => {
  return (
    <div className="flex">
      <div className="bg-gold flex-1 items-center justify-center">
        <h1>Hello World</h1>
      </div>

      <div className="flex-1">
        <h1>Hello Again</h1>
      </div>
    </div>
  );
};

export default Page;
