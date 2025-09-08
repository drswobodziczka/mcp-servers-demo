from core.claude import Claude
from mcp_client import MCPClient
from core.tools import ToolManager
from anthropic.types import MessageParam


# Czyli to jest aplikacja Chata. W pętli wymieniamy sobie wiadomosci,
# które które za każdym razem są przekazywane wraz z listą narzędzi do LLM-a.
# Aplikacja Chata dostaje również listę MCP klientów. to ciekawe, że jest to
# lista ale być może chodzi o to, że dla każdego z MCP serwerów używanych przez
# aplikację potrzebujemy mieć osobnego klienta, który otwiera połączenie i
# komunikuje się z serwerem.
#
# w szczególności jest to kawałek kodziaszku który nie jest osadzony w żadnym 
# widoku To znaczy, że aplikacja consolowa powłoka jest gdzieś indziej.
class Chat:
    def __init__(self, claude_service: Claude, clients: dict[str, MCPClient]):
        self.claude_service: Claude = claude_service
        self.clients: dict[str, MCPClient] = clients
        self.messages: list[MessageParam] = []

    async def _process_query(self, query: str):
        self.messages.append({"role": "user", "content": query})

    async def run(
        self,
        query: str,
    ) -> str:
        final_text_response = ""

        await self._process_query(query)

        while True:
            response = self.claude_service.chat(
                messages=self.messages,
                tools=await ToolManager.get_all_tools(self.clients),
            )

            self.claude_service.add_assistant_message(self.messages, response)

            if response.stop_reason == "tool_use":
                print(self.claude_service.text_from_message(response))
                tool_result_parts = await ToolManager.execute_tool_requests(
                    self.clients, response
                )

                self.claude_service.add_user_message(
                    self.messages, tool_result_parts
                )
            else:
                final_text_response = self.claude_service.text_from_message(
                    response
                )
                break

        return final_text_response
