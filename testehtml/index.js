async function cadastrarProduto(evento) {
    evento.preventDefault(); // Evita o comportamento padrão de submissão do formulário
    const input_nome = document.getElementById('nome');
    const input_preco = document.getElementById('preco');
    const input_categorias = document.getElementById('categorias');
    const input_banner = document.getElementById('banner');

    
    const nome = input_nome.value;
    const precoString = input_preco.value.replace(',', '.'); // Substitui ',' por '.' para garantir que o número seja interpretado como float
    const preco = parseFloat(precoString);
    const categorias = input_categorias.value.split(',').map(categoria => categoria.trim());
    const banner = input_banner.files[0]; // Obtém o arquivo do campo de entrada de arquivo

    // Verifica se o preço é um número float
    if (isNaN(preco) || !Number.isFinite(preco)) {
        alert('Por favor, insira um preço válido.');
        return;
    }

    try {
        await axios.post('http://localhost:5000/produtos', {
            nome: nome,
            preco: preco,
            categorias: categorias,
            banner: banner
        }, {
            headers: {
                'Content-Type': 'application/json' // Define o cabeçalho Content-Type como multipart/form-data para enviar o arquivo
            }
        }
        );
        alert('Produto cadastrado com sucesso');
    } catch (error) {
        console.error('Ocorreu um erro ao tentar cadastrar o produto:', error.response.data);
        alert('Ocorreu um erro ao tentar cadastrar o produto. Por favor, tente novamente mais tarde.');
    }
}

async function exibirProdutos() {
    try {
        const response = await axios.get('http://localhost:5000/produtos');
        const produtos = response.data;
        const lista = document.getElementById('listaProdutos');
        lista.innerHTML = '';

        produtos.forEach(produto => {
            const item = document.createElement('li');
            item.textContent = `Nome: ${produto.nome}, Preço: ${produto.preco}, Categorias: ${produto.categorias.join(', ')}`;
            lista.appendChild(item);
        });
    } catch (error) {
        console.error('Ocorreu um erro ao tentar obter os produtos:', error.response.data);
        alert('Ocorreu um erro ao tentar obter os produtos. Por favor, tente novamente mais tarde.');
    }
}

// Função para adicionar evento de submissão ao formulário
function adicionarEventoSubmit() {
    const form_produto = document.getElementById('cadastroForm');
    form_produto.onsubmit = cadastrarProduto;
}

// Chama a função para adicionar o evento de submissão ao formulário quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', adicionarEventoSubmit);

// Chama a função para exibir os produtos ao carregar a página
document.addEventListener('DOMContentLoaded', exibirProdutos);
