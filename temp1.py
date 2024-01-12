with st.spinner("Thinking..."):
        (
            full_response,
            total_tokens,
            prompt_tokens,
            completion_tokens,
        ) = generate_response(prompt)