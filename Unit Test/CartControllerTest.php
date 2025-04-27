<?php

namespace Tests\Unit;

use App\Http\Controllers\CartController;
use App\Http\Controllers\MenuController;
use App\Models\Cart;
use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Tests\TestCase;

class CartControllerTest extends TestCase
{
    use DatabaseTransactions;
    protected $cus = 'congdanhabc@outlook.com.vn';
    protected $cartAmount;
    protected function authenticate($email_user)
    {
        $user = User::where('email', $email_user)->first();
        if (!$user) {
            $this->markTestSkipped('User not found for testing.');
        }

        $this->actingAs($user);
        return $user;
    }

    public function test_cart_index()
    {
        $user = $this->authenticate($this->cus);
        // Đếm cart_amount từ database
        $controller = new CartController();
        $response = $controller->index();
        $view_name = $response->name();
        dump("View's name is: ". $view_name);
        $this->assertInstanceOf(\Illuminate\View\View::class, $response);
        $this->assertEquals('cart', $view_name);
    }

    public function test_adds_item_to_cart()
    {
        $user = $this->authenticate($this->cus);

        $product = Product::find(11);

        // Gửi yêu cầu POST đến hàm store với số lượng sản phẩm
        $response = $this->postJson(route('cart.store', ['product' => $product->id]), ['number' => 2]);

        dump("Product name: ".$product->name);

        // Kiểm tra xem sản phẩm có được thêm vào giỏ hàng không
        $this->assertDatabaseHas('carts', [
            'product_id' => $product->id,
            'user_id' => $user->id,
            'quantity' => 2,
        ]);
    }

    public function test_removes_item_to_cart()
    {
        $user = $this->authenticate($this->cus);

        $product = Product::find(11);
        dump("Product name: ".$product->name);

        // Gửi yêu cầu POST đến hàm store với số lượng sản phẩm
        $response = $this->postJson(route('cart.store', ['product' => $product]), ['number' => 2]);

        $cartItem = Cart::where('product_id', $product->id) ->where('user_id', $user->id) ->first();
        dump("Cart item id: ".$cartItem->id);

        $response1 = $this->post(route('cart.destroy', ['product' => $cartItem->id]));

        $this->assertDatabaseMissing('carts', [
            'product_id' => $product->id,
            'user_id' => $user->id,
        ]);
    }

    public function test_menu_index()
    {
        // $user = $this->authenticate($this->cus);
        $controller = new MenuController();
        $response = $controller->menu();
        $view_name = $response->name();
        dump("View's name is: ". $view_name);
        $view_data = $response->getData();
        dump("View data: ", $view_data);

        $this->assertInstanceOf(\Illuminate\View\View::class, $response);
        $this->assertEquals('menu', $view_name);
    }
}
//./vendor/bin/phpunit tests/Unit/CartControllerTest.php --filter test_menu_index
