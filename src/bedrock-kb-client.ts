// import {
//   BedrockAgentRuntimeClient,
//   RetrieveCommand,
//   RetrieveCommandInput,
//   RetrieveCommandOutput,
// } from "@aws-sdk/client-bedrock-agent-runtime";
// import { fromIni } from "@aws-sdk/credential-providers";



// export class BedrockKnowledgeBaseClient {
//   private client = new BedrockAgentRuntimeClient({
//     region: "us-east-1",
//     credentials: fromIni({ profile: "bedrock-test" })
//   });

//   async retrieveFromKnowledgeBase({ knowledgeBaseId, query, numberOfResults = 3 }) {
//     const command = new RetrieveCommand({
//       knowledgeBaseId,
//       retrievalQuery: { text: query },
//       retrievalConfiguration: {
//         vectorSearchConfiguration: {
//           numberOfResults
//         }
//       }
//     });

//     const response = await this.client.send(command);

//     return {
//       results: (response.retrievalResults || []).map(r => ({
//         content: r.content?.text || "",
//         source: r.location?.s3Location?.uri || "unknown",
//         score: r.score || 0
//       }))
//     };
//   }
// }
import {
  BedrockAgentRuntimeClient,
  RetrieveCommand,
  RetrieveCommandInput,
  RetrieveCommandOutput
} from "@aws-sdk/client-bedrock-agent-runtime";

export class BedrockKnowledgeBaseClient {
  private client: BedrockAgentRuntimeClient;

  constructor(region: string = "us-east-1") {
    this.client = new BedrockAgentRuntimeClient({ region });
  }

  async retrieveFromKnowledgeBase({
    knowledgeBaseId,
    query,
    numberOfResults = 3,
  }: {
    knowledgeBaseId: string;
    query: string;
    numberOfResults?: number;
  }): Promise<RetrieveCommandOutput> {
    const command = new RetrieveCommand({
      knowledgeBaseId,
      retrievalQuery: { text: query },  // ✅ Correct key
      retrievalConfiguration: {
        vectorSearchConfiguration: {
          numberOfResults
        }
      }
    });

    const response = await this.client.send(command);
    return response;
  }
}

