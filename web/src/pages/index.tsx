import {type NextPage} from "next";
import {CollapsibleTable} from "@/components/CollapsibleTable";
import {UploadButton} from "@/components/UploadButton";
import {useState} from "react";
import {ResultsFile} from "@/schema";

const Home: NextPage = () => {
    const [fileJson, setFileJson] = useState<ResultsFile | null>(null)
    return (
        <div className="flex flex-col items-center space-y-4 mt-4">
            <h2 className="text-2xl font-bold">Upload a results.json file</h2>
            <UploadButton setFileJson={setFileJson}/>
            {fileJson !== null && <CollapsibleTable fileJson={fileJson}/>}
        </div>
    );
};

export default Home;
