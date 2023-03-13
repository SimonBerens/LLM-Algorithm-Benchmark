import {z} from "zod";

const literalSchema = z.union([z.string(), z.number(), z.boolean(), z.null()]);
type Literal = z.infer<typeof literalSchema>;
type Json = Literal | { [key: string]: Json } | Json[];
const jsonSchema: z.ZodType<Json> = z.lazy(() =>
    z.union([literalSchema, z.array(jsonSchema), z.record(jsonSchema)])
);

export const resultsFileSchema = z.object({
    "input_texts": z.record(z.string(), z.string()),
    "code_file_strs": z.record(z.string(), z.string()),
    "task_infos": z.record(z.string(), jsonSchema),
    "results": z.array(z.object({
        "task_info_key": z.string(),
        "language": z.string(),
        "input_text_key": z.string(),
        "code_file_str_key": z.string(),
        "llm_executor_name": z.string(),
        "predicted_output": z.string(),
        "code_output": z.string(),
        "correctly_predicted": z.boolean(),
    }))
})

export type ResultsFile = z.infer<typeof resultsFileSchema>