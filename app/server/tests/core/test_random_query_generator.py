import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_random_query_with_openai,
    generate_random_query_with_anthropic,
    generate_random_query
)


class TestRandomQueryGenerator:

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_success(self, mock_openai_class):
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Show me the top 5 users by age."
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_random_query_with_openai(schema_info)

            assert result == "Show me the top 5 users by age."
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gpt-4.1-mini'
            assert call_args[1]['temperature'] == 0.8  # Higher temperature for variety
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_removes_quotes(self, mock_openai_class):
        # Test that quotes are removed from the generated query
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = '"What is the average age of users?"'
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'users': {'columns': {}, 'row_count': 10}}}

            result = generate_random_query_with_openai(schema_info)

            assert result == "What is the average age of users?"

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_single_quotes(self, mock_openai_class):
        # Test that single quotes are removed
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "'List all products sorted by price.'"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {'products': {'columns': {}, 'row_count': 50}}}

            result = generate_random_query_with_openai(schema_info)

            assert result == "List all products sorted by price."

    def test_generate_random_query_with_openai_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(schema_info)

            assert "OPENAI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_openai_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_openai(schema_info)

            assert "Error generating random query with OpenAI" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_success(self, mock_anthropic_class):
        # Mock Anthropic client and response
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = "Find all orders from the last week."
        mock_client.messages.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'orders': {
                        'columns': {'id': 'INTEGER', 'date': 'TEXT', 'total': 'REAL'},
                        'row_count': 200
                    }
                }
            }

            result = generate_random_query_with_anthropic(schema_info)

            assert result == "Find all orders from the last week."
            mock_client.messages.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.messages.create.call_args
            assert call_args[1]['model'] == 'claude-3-haiku-20240307'
            assert call_args[1]['temperature'] == 0.8  # Higher temperature for variety
            assert call_args[1]['max_tokens'] == 100

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_removes_quotes(self, mock_anthropic_class):
        # Test that quotes are removed from the generated query
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content[0].text = '"Show the top 10 customers by spending."'
        mock_client.messages.create.return_value = mock_response

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {'customers': {'columns': {}, 'row_count': 100}}}

            result = generate_random_query_with_anthropic(schema_info)

            assert result == "Show the top 10 customers by spending."

    def test_generate_random_query_with_anthropic_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(schema_info)

            assert "ANTHROPIC_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.Anthropic')
    def test_generate_random_query_with_anthropic_api_error(self, mock_anthropic_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_anthropic_class.return_value = mock_client
        mock_client.messages.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key'}):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query_with_anthropic(schema_info)

            assert "Error generating random query with Anthropic" in str(exc_info.value)

    @patch('core.llm_processor.generate_random_query_with_openai')
    def test_generate_random_query_openai_priority(self, mock_openai_func):
        # Test that OpenAI is used when OpenAI key exists
        mock_openai_func.return_value = "Show me all users."

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key', 'ANTHROPIC_API_KEY': 'anthropic-key'}):
            schema_info = {'tables': {}}

            result = generate_random_query(schema_info)

            assert result == "Show me all users."
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_random_query_with_anthropic')
    def test_generate_random_query_anthropic_fallback(self, mock_anthropic_func):
        # Test that Anthropic is used when only Anthropic key exists
        mock_anthropic_func.return_value = "List all products."

        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'anthropic-key'}, clear=True):
            schema_info = {'tables': {}}

            result = generate_random_query(schema_info)

            assert result == "List all products."
            mock_anthropic_func.assert_called_once_with(schema_info)

    def test_generate_random_query_no_api_keys(self):
        # Test error when no API keys are available
        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_random_query(schema_info)

            assert "No LLM API keys available" in str(exc_info.value)

    @patch('core.llm_processor.generate_random_query_with_openai')
    def test_generate_random_query_only_openai_key(self, mock_openai_func):
        # Test when only OpenAI key exists
        mock_openai_func.return_value = "What is the total revenue?"

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'openai-key'}, clear=True):
            schema_info = {'tables': {}}

            result = generate_random_query(schema_info)

            assert result == "What is the total revenue?"
            mock_openai_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.OpenAI')
    def test_generate_random_query_with_multiple_tables(self, mock_openai_class):
        # Test with multiple tables to ensure schema is passed correctly
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Join users and orders to show total spending per user."
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT'},
                        'row_count': 100
                    },
                    'orders': {
                        'columns': {'id': 'INTEGER', 'user_id': 'INTEGER', 'total': 'REAL'},
                        'row_count': 500
                    }
                }
            }

            result = generate_random_query_with_openai(schema_info)

            # Verify the prompt includes both tables
            call_args = mock_client.chat.completions.create.call_args
            prompt_content = call_args[1]['messages'][1]['content']
            assert 'users' in prompt_content
            assert 'orders' in prompt_content
            assert result == "Join users and orders to show total spending per user."
